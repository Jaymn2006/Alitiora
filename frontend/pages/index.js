export default function Home() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('alitiora_token') : null
  return (
    <main style={{display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',minHeight:'100vh',fontFamily:'sans-serif'}}>
      <h1>ALITIORA</h1>
      <p>AI-powered creator super-platform.</p>
      <div style={{marginTop:20}}>
        {token ? (
          <>
            <a href="/dashboard" style={{marginRight:10}}>Dashboard</a>
            <a href="/ai" style={{marginRight:10}}>AI Services</a>
            <a href="/uploads" style={{marginRight:10}}>Uploads</a>
            <a href="/messages" style={{marginRight:10}}>Messages</a>
            <a href="/payments" style={{marginRight:10}}>Payments</a>
            <a href="/profile">Profile</a>
          </>
        ) : (
          <>
            <a href="/signup" style={{marginRight:10}}>Sign up</a>
            <a href="/login">Log in</a>
          </>
        )}
      </div>
    </main>
  )
}
