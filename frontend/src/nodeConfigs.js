export const nodeConfigs = {
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
