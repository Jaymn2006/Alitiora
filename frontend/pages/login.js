import {useState} from 'react'

export default function Login(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [msg,setMsg]=useState(null)

  async function submit(e){
    e.preventDefault()
    setMsg('logging in...')
    const res = await fetch('http://localhost:8000/api/auth/login',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({email,password})})
    const data = await res.json()
    if(res.ok){
      localStorage.setItem('alitiora_token', data.token)
      setMsg('logged in')
      window.location.href = '/profile'
    } else {
      setMsg(data.detail || JSON.stringify(data))
    }
  }

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h2>Log in</h2>
      <form onSubmit={submit} style={{display:'flex',flexDirection:'column',maxWidth:400}}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button style={{marginTop:10}}>Sign in</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  )
}
