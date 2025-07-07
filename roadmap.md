# Project Roadmap

This roadmap outlines the major phases planned for NEXUS AI. Dates are estimates and may change as development progresses.

## Phase 1 – Core Platform
- Build the basic React frontend and FastAPI backend
- Implement workflow creation with a minimal set of nodes
- Provide a local execution engine with simple logging

## Phase 2 – Collaboration and Debugging
- Add real-time collaborative editing
- Introduce version control for workflows
- Expand debugging capabilities with step-by-step execution

## Phase 3 – Marketplace and Mobile
- Launch a marketplace for community workflow templates
- Develop a lightweight mobile app for monitoring

## Phase 4 – Intelligent Automation
- Integrate AI-powered suggestions for optimizing workflows
- Support auto-scaling for high-demand scenarios

### Phase 4 Progress
- Added `/workflows/{id}/suggest` endpoint providing basic workflow improvement hints
- Introduced an auto-scaling execution queue with `/workflows/{id}/enqueue`

For more detailed specifications, see [Project_Overview.md](Project_Overview.md).

