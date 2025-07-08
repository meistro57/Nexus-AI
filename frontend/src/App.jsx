/* global process */
export default function App() {
  const nodeRedUrl =
    process.env.NEXT_PUBLIC_NODE_RED_URL || 'http://localhost:1880';

  return (
    <iframe
      src={nodeRedUrl}
      style={{ width: '100%', height: '100vh', border: 'none' }}
      title="Node-RED"
    />
  );
}
