export function renderVitals(ctx, vitalsSeries) {
  const labels = vitalsSeries.map((x,i)=>`Visit ${i+1}`);
  const datasets = [
    {label:'HR', data:vitalsSeries.map(v=>parseInt(v.HR||0)), borderColor:'#ef4444', tension:.3},
    {label:'RR', data:vitalsSeries.map(v=>parseInt(v.RR||0)), borderColor:'#06b6d4', tension:.3},
    {label:'SpO2', data:vitalsSeries.map(v=>parseInt(v.SpO2||0)), borderColor:'#22c55e', tension:.3}
  ];
  return new Chart(ctx, {type:'line', data:{labels, datasets}, options:{responsive:true}});
}
