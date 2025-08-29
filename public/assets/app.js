const API = (path) => (window.API_BASE || '') + path;

// mic capture
let mediaRecorder, chunks = [];
async function startMic() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = e => chunks.push(e.data);
  mediaRecorder.onstop = async () => {
    const blob = new Blob(chunks, {type: 'audio/webm'});
    chunks = [];
    // You can POST to /api/transcribe if you connect Whisper; we forward as transcript text demo:
    document.querySelector('#transcript').value = '[Demo voice note captured. Replace with Whisper call.]';
  };
  mediaRecorder.start();
  document.querySelector('#recState').textContent = "Recording…";
}
function stopMic(){
  if(mediaRecorder && mediaRecorder.state !== 'inactive'){
    mediaRecorder.stop();
    document.querySelector('#recState').textContent = "Stopped";
  }
}

// extraction
async function extractNote(){
  const transcript = document.querySelector('#transcript').value.trim();
  if(!transcript){ alert('Please provide transcript or sample.'); return; }
  const res = await fetch(API('/api/extract'),{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ transcript })
  });
  const data = await res.json();
  const note = data.data || {};
  const fields = ['subjective','objective','assessment','plan'];
  fields.forEach(k => { const el = document.querySelector(`#${k}`); if(el) el.value = note[k] || ''; });
}

async function exportFHIR(){
  const body = {
    note:{
      subjective: document.querySelector('#subjective').value,
      objective: document.querySelector('#objective').value,
      assessment: document.querySelector('#assessment').value,
      plan: document.querySelector('#plan').value
    }
  };
  const res = await fetch(API('/api/export/fhir'), {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  const data = await res.json();
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const url  = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'),{href:url, download:'flonote-fhir.json'});
  a.click(); URL.revokeObjectURL(url);
}

async function exportCCDA(){
  const body = {
    note:{
      subjective: document.querySelector('#subjective').value,
      objective: document.querySelector('#objective').value,
      assessment: document.querySelector('#assessment').value,
      plan: document.querySelector('#plan').value
    }
  };
  const res = await fetch(API('/api/export/ccda'), {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  const { ccda } = await res.json();
  const blob = new Blob([ccda],{type:'application/xml'});
  const url  = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'),{href:url, download:'flonote-ccda.xml'});
  a.click(); URL.revokeObjectURL(url);
}