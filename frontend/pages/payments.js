import { useState } from 'react'

export default function Payments() {
  const [amount, setAmount] = useState('10')
  const [currency, setCurrency] = useState('USD')
  const [provider, setProvider] = useState('stripe_test')
  const [result, setResult] = useState(null)

  async function charge() {
    const token = localStorage.getItem('alitiora_token')
    const res = await fetch('http://localhost:8000/api/payments/charge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ amount: parseFloat(amount), currency, provider })
    })
    const data = await res.json()
    setResult(data)
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>Payments</h2>
      <div>
        <label>Amount: <input type="number" value={amount} onChange={e => setAmount(e.target.value)} /></label>
      </div>
      <div>
        <label>Currency: <select value={currency} onChange={e => setCurrency(e.target.value)}>
          <option>USD</option>
          <option>KES</option>
          <option>EUR</option>
        </select></label>
      </div>
      <div>
        <label>Provider: <select value={provider} onChange={e => setProvider(e.target.value)}>
          <option value="stripe_test">Stripe (test)</option>
          <option value="mpesa_test">M-Pesa (test)</option>
        </select></label>
      </div>
      <button onClick={charge}>Charge</button>
      {result && <pre style={{ marginTop: 10, background: '#f0f0f0', padding: 10 }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}
