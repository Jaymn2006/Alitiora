import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    const token = localStorage.getItem('alitiora_token')
    if (!token) return
    Promise.all([
      fetch('http://localhost:8000/api/users/me', { headers: { 'Authorization': 'Bearer ' + token } }).then(r => r.json()),
    ]).then(([user]) => {
      setStats({ user: user.user })
    })
  }, [])

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>Dashboard</h2>
      {stats ? (
        <div>
          <p><b>Name:</b> {stats.user.name}</p>
          <p><b>Email:</b> {stats.user.email}</p>
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/ai">AI Services</a></li>
            <li><a href="/uploads">Uploads</a></li>
            <li><a href="/messages">Messages</a></li>
            <li><a href="/payments">Payments</a></li>
          </ul>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  )
}
