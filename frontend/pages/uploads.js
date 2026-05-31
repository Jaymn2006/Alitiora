import { useState, useEffect } from 'react'

export default function Uploads() {
  const [file, setFile] = useState(null)
  const [uploads, setUploads] = useState([])
  const [result, setResult] = useState(null)

  async function handleUpload() {
    if (!file) return
    const token = localStorage.getItem('alitiora_token')
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch('http://localhost:8000/api/uploads', { method: 'POST', headers: { 'Authorization': 'Bearer ' + token }, body: fd })
    const data = await res.json()
    setResult(data)
    setFile(null)
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>Uploads</h2>
      <input type="file" onChange={e => setFile(e.target.files?.[0])} />
      <button onClick={handleUpload}>Upload</button>
      {result && <pre style={{ marginTop: 10, background: '#f0f0f0', padding: 10 }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
