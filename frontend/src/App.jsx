import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/health')
      .then(res => res.json())
      .then(data => {
        setHealth(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="app">
      <header>
        <h1>tensor-lab-145</h1>
        <p>CLI-Anything: Making ALL Software Agent-Native</p>
      </header>
      <main>
        <section className="health-check">
          <h2>Backend Health</h2>
          <pre>{JSON.stringify(health, null, 2)}</pre>
        </section>
        <section className="cli-generator">
          <h2>CLI Generator</h2>
          <p>Source code analysis and CLI generation coming soon...</p>
        </section>
      </main>
    </div>
  )
}

export default App
