from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Vital(BaseModel):
    name: str
    value: str

class Note(BaseModel):
    id: str
    patient_name: Optional[str] = None
    template_slug: str
    conditions: List[str] = Field(default_factory=list)
    transcript: str = ""
    subjective: str = ""
    objective: str = ""
    assessment: str = ""
    plan: str = ""
    vitals: List[Vital] = Field(default_factory=list)
    variables: Dict[str, str] = Field(default_factory=dict)

class TemplateItem(BaseModel):
    title: str
    slug: str
    type: str   # soap, hp, progress, condition
    description: Optional[str] = None
    variables: List[str] = Field(default_factory=list)
    guideline_links: List[str] = Field(default_factory=list)

class ExtractRequest(BaseModel):
    transcript: str
    template_slug: str
    conditions: List[str] = Field(default_factory=list)
    patient_name: Optional[str] = None
    history: Optional[Dict[str, Any]] = None

class ExportRequest(BaseModel):
    note: Note
    format: str  # fhir or ccda
    patient_id: Optional[str] = None
