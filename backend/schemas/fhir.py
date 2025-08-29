def note_to_fhir(note, patient_id="TEMP123"):
    return {
      "resourceType":"Bundle","type":"document","entry":[
        {"resource":{"resourceType":"Patient","id":patient_id,"name":[{"text":note.patient_name or "Unknown"}]}},
        {"resource":{"resourceType":"Composition","status":"final","type":{"text":"Clinical Note"},
          "subject":{"reference":f"Patient/{patient_id}"},"title":"Clinical Documentation",
          "section":[
            {"title":"Subjective","text":{"status":"generated","div":f"<div>{note.subjective}</div>"}},
            {"title":"Objective","text":{"status":"generated","div":f"<div>{note.objective}</div>"}},
            {"title":"Assessment","text":{"status":"generated","div":f"<div>{note.assessment}</div>"}},
            {"title":"Plan","text":{"status":"generated","div":f"<div>{note.plan}</div>"}}]}}]}
