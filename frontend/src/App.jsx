import { useState } from 'react'
import './App.css'

function App() {
  const [logs, setLogs] = useState([])

  const runWorkflow = async () => {
    const workflow = {
      id: 'demo',
      name: 'Demo Workflow',
      nodes: [
        { id: '1', type: 'print', params: { message: 'Hello from NEXUS' } },
        { id: '2', type: 'add', params: { a: 2, b: 3 } }
      ]
    }

    await fetch('http://localhost:8000/workflows', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workflow)
    })

    const res = await fetch(`http://localhost:8000/workflows/${workflow.id}/execute`, {
      method: 'POST'
    })

    const data = await res.json()
    setLogs(data.logs || [])
  }

  return (
    <div className="container">
      <h1>NEXUS AI</h1>
      <button onClick={runWorkflow}>Run Demo Workflow</button>
      <pre>{logs.join('\n')}</pre>
    </div>
  )
}

export default App
