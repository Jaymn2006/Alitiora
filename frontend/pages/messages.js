import { useState, useEffect } from 'react'

export default function Messages() {
  const [to_id, setToId] = useState('')
  const [body, setBody] = useState('')
  const [messages, setMessages] = useState([])

  async function sendMessage() {
    const token = localStorage.getItem('alitiora_token')
    const res = await fetch('http://localhost:8000/api/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ to_id, body })
    })
    const data = await res.json()
    setBody('')
    loadMessages()
  }

  async function loadMessages() {
    const token = localStorage.getItem('alitiora_token')
    const res = await fetch('http://localhost:8000/api/messages', { headers: { 'Authorization': 'Bearer ' + token } })
    const data = await res.json()
    setMessages(data.messages || [])
  }

  useEffect(() => { loadMessages() }, [])

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>Messages</h2>
      <input placeholder="To ID" value={to_id} onChange={e => setToId(e.target.value)} />
      <textarea placeholder="Message body" value={body} onChange={e => setBody(e.target.value)} style={{ width: '100%', height: 80, marginBottom: 10 }} />
      <button onClick={sendMessage}>Send</button>
      <div style={{ marginTop: 20 }}>
        <h3>Messages ({messages.length})</h3>
        {messages.map(m => <div key={m.id} style={{ background: '#f0f0f0', padding: 10, marginBottom: 5 }}>{m.from_id} → {m.to_id}: {m.body}</div>)}
      </div>
    </div>
  )
}
