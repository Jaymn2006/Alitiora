import { useState } from 'react'

export default function AI() {
  const [service, setService] = useState('code_generator')
  const [input, setInput] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function callAI() {
    setLoading(true)
    const token = localStorage.getItem('alitiora_token')
    try {
      const res = await fetch(`http://localhost:8000/api/ai/${service}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ input })
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      setResult({ error: e.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>AI Services</h2>
      <select value={service} onChange={e => setService(e.target.value)} style={{ marginBottom: 10 }}>
        <option value="code_generator">Code Generator</option>
        <option value="content_assistant">Content Assistant</option>
        <option value="media_processor">Media Processor</option>
        <option value="recommendation_engine">Recommendation Engine</option>
        <option value="mentor_ai">Mentor AI</option>
        <option value="ip_protection_ai">IP Protection</option>
        <option value="payments_advisor">Payments Advisor</option>
        <option value="moderation_ai">Moderation</option>
      </select>
      <textarea value={input} onChange={e => setInput(e.target.value)} placeholder="Input" style={{ width: '100%', height: 100, marginBottom: 10 }} />
      <button onClick={callAI} disabled={loading}>{loading ? 'Processing...' : 'Run'}</button>
      {result && <pre style={{ marginTop: 10, background: '#f0f0f0', padding: 10 }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
