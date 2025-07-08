import React from 'react'
import { useWorkflowStore } from './store.js'

export default function ExecutionControls() {
  const { nodes } = useWorkflowStore()

  const runWorkflow = async () => {
    const workflow = {
      id: 'wf1',
      name: 'UI Workflow',
      nodes: nodes.map(n => ({
        id: n.id,
        type: n.data.type,
        params: n.data.properties || {}
      }))
    }
    try {
      await fetch('http://localhost:8000/workflows', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer testtoken'
        },
        body: JSON.stringify(workflow)
      })
      await fetch(`http://localhost:8000/workflows/${workflow.id}/execute`, {
        method: 'POST',
        headers: { Authorization: 'Bearer testtoken' }
      })
    } catch (err) {
      console.error('Failed to execute workflow', err)
    }
  }

  return (
    <div style={{ padding: 8 }}>
      <button onClick={runWorkflow}>Run Workflow</button>
    </div>
  )
}
