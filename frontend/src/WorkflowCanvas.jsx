import { useCallback, useRef, useState } from 'react'
import ReactFlow, {
  ReactFlowProvider,
  addEdge as reactAddEdge,
  applyEdgeChanges,
  applyNodeChanges
} from 'reactflow'
import 'reactflow/dist/style.css'
import NodePalette from './NodePalette.jsx'
import { nodeConfigs } from './nodeConfigs.js'
import { useWorkflowStore } from './store.js'
import LogPanel from './LogPanel.jsx'

let id = 0
const getId = () => `node_${id++}`

export default function WorkflowCanvas() {
  const reactFlowWrapper = useRef(null)
  const [reactFlowInstance, setReactFlowInstance] = useState(null)
  const { nodes, edges, setNodes, setEdges, addNode, addEdge } =
    useWorkflowStore()

  const onNodesChange = useCallback(
    changes => setNodes(applyNodeChanges(changes, nodes)),
    [nodes]
  )
  const onEdgesChange = useCallback(
    changes => setEdges(applyEdgeChanges(changes, edges)),
    [edges]
  )
  const onConnect = useCallback(
    params => setEdges(reactAddEdge(params, edges)),
    [edges]
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
      addNode(newNode)
    },
    [reactFlowInstance]
  )

  const handleDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <NodePalette onDragStart={handleDragStart} />
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
        <LogPanel />
      </div>
    </div>
  )
}
