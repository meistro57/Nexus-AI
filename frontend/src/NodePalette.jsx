import React, { useState, useMemo } from 'react'
import { nodeConfigs } from './nodeConfigs.js'

export default function NodePalette({ onDragStart }) {
  const [search, setSearch] = useState('')
  const filteredNodes = useMemo(
    () =>
      Object.entries(nodeConfigs).filter(([, cfg]) =>
        cfg.title.toLowerCase().includes(search.toLowerCase())
      ),
    [search]
  )

  return (
    <div style={{ width: 200, padding: 10, background: '#111', color: '#fff' }}>
      <input
        type="text"
        placeholder="Search..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{ width: '100%', marginBottom: 8 }}
      />
      {filteredNodes.map(([type, cfg]) => (
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
