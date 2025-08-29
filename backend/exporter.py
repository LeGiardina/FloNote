import os, httpx, json
from .schemas.fhir import note_to_fhir
from .schemas.ccda import note_to_ccda
EHR_EXPORT_URL=os.getenv("EHR_EXPORT_URL","")
async def export_note(note, fmt="fhir", patient_id="TEMP123"):
    if fmt=="fhir":
        payload=note_to_fhir(note, patient_id)
        ctype, body="application/fhir+json", json.dumps(payload)
    else:
        body=note_to_ccda(note, patient_id)
        ctype="application/xml"
    if EHR_EXPORT_URL:
        async with httpx.AsyncClient(timeout=60) as cli:
            await cli.post(EHR_EXPORT_URL, headers={"Content-Type":ctype}, content=body)
    return ctype, body
