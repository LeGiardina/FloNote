import json, uuid, os
from typing import List
from .models import Note, TemplateItem

DATA_DIR = os.path.join(os.path.dirname(__file__), "templates")
NOTES_PATH = os.path.join(DATA_DIR, "seed_notes.json")
LIB_PATH   = os.path.join(DATA_DIR, "library.json")

def _load(path:str, default):
    if not os.path.exists(path): return default
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def _save(path:str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: json.dump(obj, f, indent=2)

def list_templates()->List[TemplateItem]:
    return [TemplateItem(**t) for t in _load(LIB_PATH, [])]

def add_or_update_template(t:TemplateItem):
    lib=_load(LIB_PATH, [])
    existing = next((x for x in lib if x.get("slug")==t.slug), None)
    if existing: existing.update(t.model_dump())
    else: lib.append(t.model_dump())
    _save(LIB_PATH, lib)

def save_note(n:Note):
    db=_load(NOTES_PATH, [])
    found=next((x for x in db if x.get("id")==n.id), None)
    if found: found.update(n.model_dump())
    else: db.append(n.model_dump())
    _save(NOTES_PATH, db)

def list_notes()->List[Note]:
    return [Note(**n) for n in _load(NOTES_PATH, [])]

def new_note_id()->str:
    return str(uuid.uuid4())[:8]
