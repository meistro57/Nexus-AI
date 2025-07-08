import { useEffect, useState } from 'react'

export default function LogPanel() {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/logs')
    ws.onmessage = evt => setLogs(l => [...l, evt.data])
    return () => ws.close()
  }, [])

  return (
    <div style={{ height: 200, overflow: 'auto', background: '#000', color: '#0f0', padding: 8 }}>
      {logs.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  )
}
