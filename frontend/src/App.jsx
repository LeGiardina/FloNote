import React, { useEffect, useState } from 'react'

export default function App() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/health')
      .then(r => r.json())
      .then(setHealth)
      .catch(err => setHealth({ error: String(err) }))
  }, [])

  return (
    <div style={{ fontFamily: 'system-ui, Arial', padding: 24 }}>
      <h1>FloNote — Medical Scribe</h1>
      <p>If you can read this, the SPA is served from <code>/</code>.</p>
      <h3>API Health</h3>
      <pre>{JSON.stringify(health, null, 2)}</pre>
      <p>Try the API docs at <a href="/docs">/docs</a>.</p>
    </div>
  )
}
