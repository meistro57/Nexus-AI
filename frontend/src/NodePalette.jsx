import React from 'react'
import { nodeConfigs } from './nodeConfigs.js'

export default function NodePalette({ onDragStart }) {
  return (
    <div style={{ width: 200, padding: 10, background: '#111', color: '#fff' }}>
      {Object.entries(nodeConfigs).map(([type, cfg]) => (
        <div
          key={type}
          onDragStart={e => onDragStart(e, type)}
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
  )
}
