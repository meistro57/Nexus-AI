import { create } from 'zustand'

export const useWorkflowStore = create(set => ({
  nodes: [],
  edges: [],
  selectedNode: null,
  setNodes: nodes => set({ nodes }),
  setEdges: edges => set({ edges }),
  addNode: node => set(state => ({ nodes: [...state.nodes, node] })),
  addEdge: edge => set(state => ({ edges: [...state.edges, edge] })),
  selectNode: nodeId => set({ selectedNode: nodeId }),
  updateNode: (id, updates) =>
    set(state => ({
      nodes: state.nodes.map(n => (n.id === id ? { ...n, ...updates } : n))
    }))
}))
