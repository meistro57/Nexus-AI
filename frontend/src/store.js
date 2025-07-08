import { create } from 'zustand'

export const useWorkflowStore = create(set => ({
  nodes: [],
  edges: [],
  setNodes: nodes => set({ nodes }),
  setEdges: edges => set({ edges }),
  addNode: node => set(state => ({ nodes: [...state.nodes, node] })),
  addEdge: edge => set(state => ({ edges: [...state.edges, edge] }))
}))
