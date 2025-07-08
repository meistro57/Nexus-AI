# Project Roadmap

This roadmap outlines the major phases planned for NEXUS AI. Dates are estimates and may change as development progresses.

## Phase 1 – Core Platform
- Build the basic React frontend and FastAPI backend
- Implement workflow creation with a minimal set of nodes
- Provide a local execution engine with simple logging

### Phase 1 Status
- Initial node types (`print`, `add`, `delay`, `condition`, `loop`) implemented
- Basic execution engine and REST APIs working

## Phase 2 – Collaboration and Debugging
- Add real-time collaborative editing
- Introduce version control for workflows
- Expand debugging capabilities with step-by-step execution

### Phase 2 Progress
- Workflow update and delete endpoints
- Workflow validation and disk persistence
- New `multiply` node and ReactFlow-based UI

## Phase 3 – Marketplace and Mobile
- Launch a marketplace for community workflow templates
- Develop a lightweight mobile app for monitoring

## Phase 4 – Intelligent Automation
- Integrate AI-powered suggestions for optimizing workflows
- Support auto-scaling for high-demand scenarios

### Phase 4 Progress
- Added `/workflows/{id}/suggest` endpoint providing basic workflow improvement hints
- Introduced an auto-scaling execution queue with `/workflows/{id}/enqueue`

For more detailed specifications, see [AGENTS.md](AGENTS.md).

## Phase 5 – Polish & Optimization
- Performance optimization
- UI/UX refinements
- Comprehensive testing
- Documentation completion
- Deployment setup

## Next Steps – Features for a Functioning Product
The following items will bring NEXUS AI from prototype to a usable application:

- Convert the current static HTML into reusable React components.
- Introduce global state management (e.g. Redux or Zustand) for workflows.
- Provide real-time WebSocket updates for execution status and logs.
- Add robust validation and error handling for all node types.
- Implement authentication and authorization across the API.

