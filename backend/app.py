from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, datetime
from typing import Optional, List, Dict

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = FastAPI(title="FloNote V2 API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ExtractRequest(BaseModel):
    transcript: str
    demographics: Optional[Dict] = None
    problems: Optional[List[str]] = None
    template: Optional[str] = "SOAP"

def _rule_based_extract(text: str) -> Dict:
    # a tiny heuristic fallback
    def grab(marker):
        import re
        m = re.search(rf"{marker}:(.*?)(?=$|\n[A-Z][A-Za-z ]+:)", text, flags=re.S|re.M)
        return m.group(1).strip() if m else ""
    return {
        "subjective": grab("Subjective") or text[:400],
        "objective": grab("Objective"),
        "assessment": grab("Assessment"),
        "plan": grab("Plan"),
        "vitals": {"bp_sys": "", "bp_dia": "", "hr": "", "rr": "", "temp_c": "", "spo2": ""}
    }

@app.post("/api/extract")
def extract(req: ExtractRequest):
    if OPENAI_API_KEY and OpenAI is not None:
        client = OpenAI(api_key=OPENAI_API_KEY)
        system = "You structure clinical dictations into SOAP fields. Return JSON keys: subjective, objective, assessment, plan, vitals."
        prompt = f"Transcript:\n{req.transcript}\nReturn JSON only."
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
                temperature=0.2
            )
            import json as _json
            content = resp.choices[0].message.content
            # try parse json block
            start = content.find("{")
            end   = content.rfind("}")
            data = _json.loads(content[start:end+1])
            return {"ok": True, "data": data, "llm": "openai"}
        except Exception as e:
            # fall back
            data = _rule_based_extract(req.transcript)
            return {"ok": True, "data": data, "fallback": str(e)}
    else:
        data = _rule_based_extract(req.transcript)
        return {"ok": True, "data": data, "llm": "rule"}

class ExportRequest(BaseModel):
    note: Dict
    patient: Optional[Dict] = None

@app.post("/api/export/fhir")
def export_fhir(req: ExportRequest):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    bundle = {
        "resourceType": "Bundle",
        "type": "document",
        "timestamp": now,
        "entry": [
            {"resource": {"resourceType":"Composition","status":"final","type":{"text":"Clinical Note"},
                          "date":now,"title":"FloNote Document"}},
            {"resource": {"resourceType":"Observation","status":"final","code":{"text":"Subjective"},
                          "valueString": req.note.get("subjective","")}},
            {"resource": {"resourceType":"Observation","status":"final","code":{"text":"Objective"},
                          "valueString": req.note.get("objective","")}},
            {"resource": {"resourceType":"Observation","status":"final","code":{"text":"Assessment"},
                          "valueString": req.note.get("assessment","")}},
            {"resource": {"resourceType":"Observation","status":"final","code":{"text":"Plan"},
                          "valueString": req.note.get("plan","")}},
        ]
    }
    return bundle

@app.post("/api/export/ccda")
def export_ccda(req: ExportRequest):
    # minimalist CCDA-like XML
    subj = req.note.get("subjective","").replace("&","&amp;")
    obj  = req.note.get("objective","").replace("&","&amp;")
    asm  = req.note.get("assessment","").replace("&","&amp;")
    plan = req.note.get("plan","").replace("&","&amp;")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument>
  <title>FloNote CCD</title>
  <section><code displayName="Subjective"/><text>{subj}</text></section>
  <section><code displayName="Objective"/><text>{obj}</text></section>
  <section><code displayName="Assessment"/><text>{asm}</text></section>
  <section><code displayName="Plan"/><text>{plan}</text></section>
</ClinicalDocument>"""
    return {"ccda": xml}

@app.get("/api/templates")
def get_templates():
    # shipped starter set
    return {
        "default": ["SOAP Note","H&P Note","Progress Note"],
        "conditions": ["COPD Exacerbation","Asthma","Diabetes Mellitus Type 2","Congestive Heart Failure"]
    }

@app.get("/healthz")
def healthz():
    return {"ok": True}