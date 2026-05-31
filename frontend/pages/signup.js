import {useState} from 'react'

export default function Signup(){
  const [name,setName]=useState('')
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [msg,setMsg]=useState(null)

  async function submit(e){
    e.preventDefault()
    setMsg('creating...')
    const res = await fetch('http://localhost:8000/api/auth/signup',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({name,email,password})})
    const data = await res.json()
    if(res.ok){
      setMsg('created; please login')
    } else {
      setMsg(data.detail || JSON.stringify(data))
    }
  }

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h2>Sign up</h2>
      <form onSubmit={submit} style={{display:'flex',flexDirection:'column',maxWidth:400}}>
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button style={{marginTop:10}}>Create account</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  )
}
