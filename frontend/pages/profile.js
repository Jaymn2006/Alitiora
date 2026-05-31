import {useEffect, useState} from 'react'

export default function Profile(){
  const [user,setUser]=useState(null)
  const [msg,setMsg]=useState(null)

  useEffect(()=>{
    const token = localStorage.getItem('alitiora_token')
    if(!token){
      setMsg('not logged in')
      return
    }
    fetch('http://localhost:8000/api/users/me',{headers:{'Authorization': 'Bearer '+token}})
      .then(r=>r.json())
      .then(d=>{
        if(d.user) setUser(d.user)
        else setMsg(d.detail || JSON.stringify(d))
      })
  },[])

  function logout(){
    const token = localStorage.getItem('alitiora_token')
    fetch('http://localhost:8000/api/auth/logout',{method:'POST',headers:{'Authorization':'Bearer '+token}})
      .finally(()=>{
        localStorage.removeItem('alitiora_token')
        window.location.href = '/'
      })
  }

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h2>Profile</h2>
      {user ? (
        <div>
          <p><b>Name:</b> {user.name}</p>
          <p><b>Email:</b> {user.email}</p>
          <button onClick={logout}>Log out</button>
        </div>
      ) : (
        <p>{msg || 'loading...'}</p>
      )}
    </div>
  )
}
