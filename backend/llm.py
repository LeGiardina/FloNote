import os, httpx, json
from pydantic import BaseModel
from .models import ExtractRequest

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
MODEL_TEXT=os.getenv("MODEL_TEXT","gpt-4o-mini")
MODEL_AUDIO=os.getenv("MODEL_AUDIO","whisper-1")

class LLMClient(BaseModel):
    api_key: str = OPENAI_API_KEY

    async def whisper_transcribe(self, audio_bytes:bytes, filename:str)->str:
        if not self.api_key:
            return ""
        url="https://api.openai.com/v1/audio/transcriptions"
        files={"file":(filename,audio_bytes,"audio/webm")}
        data={"model":MODEL_AUDIO}
        headers={"Authorization":f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=120) as cli:
            r=await cli.post(url, headers=headers, data=data, files=files)
            r.raise_for_status()
            j=r.json()
            return j.get("text","")

    async def extract_structured(self, req:ExtractRequest):
        if not self.api_key:
            # fallback: naive sections
            return {"subjective":"","objective":"","assessment":"","plan":"","vitals":[]}
        system="You turn clinical dictation into concise, structured SOAP JSON."
        user=f"""Transcript:\n{req.transcript}\n\nTemplate slug: {req.template_slug}\nKnown conditions: {', '.join(req.conditions) or 'none'}\nReturn keys: subjective, objective, assessment, plan, vitals (array of objects with name,value). Keep medical register, be concise."""
        url="https://api.openai.com/v1/chat/completions"
        headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}
        payload={"model":MODEL_TEXT,"messages":[{"role":"system","content":system},{"role":"user","content":user}],
                 "temperature":0.2,"response_format":{"type":"json_object"}}
        async with httpx.AsyncClient(timeout=120) as cli:
            r=await cli.post(url, headers=headers, json=payload)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
