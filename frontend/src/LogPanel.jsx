import { useEffect, useState } from 'react'

export default function LogPanel() {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    let socket
    let shouldReconnect = true

    const connect = () => {
      socket = new WebSocket('ws://localhost:8000/ws/logs')
      socket.onmessage = evt => setLogs(l => [...l, evt.data])
      socket.onerror = () => socket.close()
      socket.onclose = () => {
        if (shouldReconnect) setTimeout(connect, 1000)
      }
    }

    connect()

    return () => {
      shouldReconnect = false
      socket?.close()
    }
  }, [])

  return (
    <div style={{ height: 200, overflow: 'auto', background: '#000', color: '#0f0', padding: 8 }}>
      {logs.map((l, i) => (
        <div key={i}>{l}</div>
      ))}
    </div>
  )
}
