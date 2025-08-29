from xml.sax.saxutils import escape
def note_to_ccda(note, patient_id="TEMP123"):
    def block(t,b): return f"<section><title>{escape(t)}</title><text>{escape(b or '')}</text></section>"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <id root="{escape(note.id)}"/>
  <recordTarget><patientRole><id extension="{escape(patient_id)}"/>
  <patient><name><given>{escape((note.patient_name or 'Unknown').split(' ')[0])}</given></name></patient>
  </patientRole></recordTarget>
  <component><structuredBody>
    {block("Subjective", note.subjective)}
    {block("Objective", note.objective)}
    {block("Assessment", note.assessment)}
    {block("Plan", note.plan)}
  </structuredBody></component>
</ClinicalDocument>"""
