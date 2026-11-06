import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [analyzeLoading, setAnalyzeLoading] = useState(false)
  const [analyzeError, setAnalyzeError] = useState(null)
  const [sourcePath, setSourcePath] = useState('')

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

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setAnalyzeLoading(true)
    setAnalyzeError(null)
    setAnalysis(null)
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_path: sourcePath })
      })
      const data = await response.json()
      if (data.error) {
        setAnalyzeError(data.error)
      } else {
        setAnalysis(data)
      }
    } catch (err) {
      setAnalyzeError(err.message)
    } finally {
      setAnalyzeLoading(false)
    }
  }

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
          <h2>Code Analysis & CLI Generator</h2>
          <form onSubmit={handleAnalyze} style={{ marginBottom: '1rem' }}>
            <label>
              Source Path:
              <input
                type="text"
                value={sourcePath}
                onChange={(e) => setSourcePath(e.target.value)}
                placeholder="/path/to/python/project"
                style={{ width: '60%', marginLeft: '0.5rem', marginRight: '0.5rem' }}
              />
            </label>
            <button type="submit" disabled={analyzeLoading || !sourcePath}>
              {analyzeLoading ? 'Analyzing...' : 'Analyze'}
            </button>
          </form>
          {analyzeError && <div className="error">Error: {analyzeError}</div>}
          {analysis && (
            <div className="analysis-results">
              <details open>
                <summary>Functions ({analysis.functions?.length || 0})</summary>
                <pre>{JSON.stringify(analysis.functions, null, 2)}</pre>
              </details>
              <details open>
                <summary>Classes ({analysis.classes?.length || 0})</summary>
                <pre>{JSON.stringify(analysis.classes, null, 2)}</pre>
              </details>
              <details open>
                <summary>Entry Points ({analysis.entry_points?.length || 0})</summary>
                <pre>{JSON.stringify(analysis.entry_points, null, 2)}</pre>
              </details>
              <details open>
                <summary>Generated CLI Commands ({analysis.commands?.length || 0})</summary>
                <pre>{JSON.stringify(analysis.commands, null, 2)}</pre>
              </details>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
