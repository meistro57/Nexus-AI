import { useCallback, useRef, useState } from 'react'
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges
} from 'reactflow'
import 'reactflow/dist/style.css'

const nodeConfigs = {
  'llama-chat': {
    title: 'Llama Chat Agent',
    icon: '🦙',
    description: 'Local Llama instance for conversational AI',
    properties: {
      model: 'llama-3.2-3b',
      temperature: 0.7,
      max_tokens: 2048,
      system_prompt: 'You are a helpful AI assistant.'
    }
  },
  'code-agent': {
    title: 'Code Generator',
    icon: '💻',
    description: 'Specialized coding assistant agent',
    properties: {
      language: 'python',
      style: 'clean',
      include_comments: true
    }
  },
  'research-agent': {
    title: 'Research Agent',
    icon: '🔬',
    description: 'Web research and data analysis',
    properties: {
      max_sources: 5,
      depth: 'moderate',
      include_citations: true
    }
  },
  'data-input': {
    title: 'Data Input',
    icon: '📥',
    description: 'File, text, or API data source',
    properties: {
      source_type: 'file',
      file_path: '',
      encoding: 'utf-8'
    }
  },
  condition: {
    title: 'Condition',
    icon: '🔀',
    description: 'Conditional branching logic',
    properties: {
      condition: 'value > 0',
      operator: 'greater_than'
    }
  }
}

let id = 0
const getId = () => `node_${id++}`

export default function WorkflowCanvas() {
  const reactFlowWrapper = useRef(null)
  const [reactFlowInstance, setReactFlowInstance] = useState(null)
  const [nodes, setNodes] = useState([])
  const [edges, setEdges] = useState([])

  const onNodesChange = useCallback(
    changes => setNodes(nds => applyNodeChanges(changes, nds)),
    []
  )
  const onEdgesChange = useCallback(
    changes => setEdges(eds => applyEdgeChanges(changes, eds)),
    []
  )
  const onConnect = useCallback(
    params => setEdges(eds => addEdge(params, eds)),
    []
  )

  const onDragOver = useCallback(event => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  const onDrop = useCallback(
    event => {
      event.preventDefault()
      const type = event.dataTransfer.getData('application/reactflow')
      if (!type || !reactFlowInstance) return
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowWrapper.current.getBoundingClientRect().left,
        y: event.clientY - reactFlowWrapper.current.getBoundingClientRect().top
      })
      const config = nodeConfigs[type] || { title: type }
      const newNode = {
        id: getId(),
        type: 'default',
        position,
        data: { label: config.title, type, properties: config.properties }
      }
      setNodes(nds => nds.concat(newNode))
    },
    [reactFlowInstance]
  )

  const handleDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div
        style={{ width: 200, padding: 10, background: '#111', color: '#fff' }}
      >
        {Object.entries(nodeConfigs).map(([type, cfg]) => (
          <div
            key={type}
            onDragStart={e => handleDragStart(e, type)}
            draggable
            style={{
              marginBottom: 8,
              border: '1px solid #555',
              padding: 6,
              cursor: 'grab'
            }}
          >
            {cfg.icon} {cfg.title}
          </div>
        ))}
      </div>
      <div style={{ flex: 1 }} ref={reactFlowWrapper}>
        <ReactFlowProvider>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onInit={setReactFlowInstance}
            fitView
          />
        </ReactFlowProvider>
      </div>
    </div>
  )
}
