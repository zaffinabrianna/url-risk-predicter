import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const analyzeUrl = async () => {
    if (!url) return

    setIsLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `url=${encodeURIComponent(url)}`
      })

      const data = await response.json()
      console.log('API Response:', data) 
      setResult(data)
    } catch (err) {
      console.error('Error:', err) 
      setError('Failed to analyze URL. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>🔒 LinkShield</h1>
      <p>Smart Malicious URL Checker</p>
      
      <div style={{ marginTop: '20px' }}>
        <input
          type="text"
          placeholder="Enter URL to analyze..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="input"
          style={{ marginBottom: '10px' }}
        />
        <br />
        <button 
          onClick={analyzeUrl}
          disabled={isLoading || !url}
          className="btn btn-primary"
        >
          {isLoading ? 'Analyzing...' : 'Analyze URL'}
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginTop: '20px' }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h2>Analysis Results</h2>
          <div style={{ 
            padding: '15px', 
            border: '1px solid #ccc', 
            borderRadius: '5px',
            backgroundColor: '#f9f9f9'
          }}>
            <p><strong>Risk Level:</strong> {result.risk_level || 'Unknown'}</p>
            <p><strong>Risk Score:</strong> {typeof result.risk_score === 'number' ? (result.risk_score * 100).toFixed(1) + '%' : 'Unknown'}</p>
            {result.risk_factors && result.risk_factors.length > 0 && (
              <div>
                <strong>Risk Factors:</strong>
                <ul>
                  {result.risk_factors.map((factor: string, index: number) => (
                    <li key={index}>{factor}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App