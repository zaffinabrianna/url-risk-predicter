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
      setResult(data)
    } catch (err) {
      setError('Failed to analyze URL. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const getRiskColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'Safe':
        return '#10b981'
      case 'Low Risk':
        return '#f59e0b'
      case 'Medium Risk':
        return '#f97316'
      case 'High Risk':
        return '#ef4444'
      default:
        return '#6b7280'
    }
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f8fafc',
      padding: '20px'
    }}>
      <div style={{ 
        maxWidth: '800px', 
        margin: '0 auto',
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        padding: '40px'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ 
            fontSize: '2.5rem', 
            fontWeight: 'bold', 
            color: '#1f2937',
            marginBottom: '8px'
          }}>
            🔒 LinkShield
          </h1>
          <p style={{ 
            fontSize: '1.1rem', 
            color: '#6b7280',
            margin: '0'
          }}>
            Smart Malicious URL Checker
          </p>
        </div>
        
        <div style={{ marginBottom: '30px' }}>
          <div style={{ 
            display: 'flex', 
            gap: '12px',
            marginBottom: '20px'
          }}>
            <input
              type="text"
              placeholder="Enter URL to analyze (e.g., https://example.com)..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{
                flex: 1,
                padding: '12px 16px',
                border: '2px solid #e5e7eb',
                borderRadius: '8px',
                fontSize: '16px',
                outline: 'none',
                transition: 'border-color 0.2s'
              }}
              onFocus={(e) => e.target.style.borderColor = '#3b82f6'}
              onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
            />
            <button 
              onClick={analyzeUrl}
              disabled={isLoading || !url}
              style={{
                padding: '12px 24px',
                backgroundColor: isLoading || !url ? '#9ca3af' : '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: isLoading || !url ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.2s'
              }}
            >
              {isLoading ? 'Analyzing...' : 'Analyze URL'}
            </button>
          </div>
        </div>

        {error && (
          <div style={{ 
            padding: '12px 16px',
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '8px',
            color: '#dc2626',
            marginBottom: '20px'
          }}>
            {error}
          </div>
        )}

        {result && (
          <div style={{ 
            backgroundColor: '#f9fafb',
            borderRadius: '12px',
            padding: '24px',
            border: '1px solid #e5e7eb'
          }}>
            <h2 style={{ 
              fontSize: '1.5rem', 
              fontWeight: '600', 
              color: '#1f2937',
              marginBottom: '20px'
            }}>
              Analysis Results
            </h2>
            
            <div style={{ 
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '20px',
              marginBottom: '20px'
            }}>
              <div style={{ 
                padding: '16px',
                backgroundColor: 'white',
                borderRadius: '8px',
                border: '1px solid #e5e7eb'
              }}>
                <p style={{ 
                  margin: '0 0 8px 0',
                  fontSize: '14px',
                  color: '#6b7280',
                  fontWeight: '500'
                }}>
                  Risk Level
                </p>
                <p style={{ 
                  margin: '0',
                  fontSize: '18px',
                  fontWeight: '600',
                  color: getRiskColor(result.risk_level)
                }}>
                  {result.risk_level || 'Unknown'}
                </p>
              </div>
              
              <div style={{ 
                padding: '16px',
                backgroundColor: 'white',
                borderRadius: '8px',
                border: '1px solid #e5e7eb'
              }}>
                <p style={{ 
                  margin: '0 0 8px 0',
                  fontSize: '14px',
                  color: '#6b7280',
                  fontWeight: '500'
                }}>
                  Risk Score
                </p>
                <p style={{ 
                  margin: '0',
                  fontSize: '18px',
                  fontWeight: '600',
                  color: getRiskColor(result.risk_level)
                }}>
                  {typeof result.risk_score === 'number' ? (result.risk_score * 100).toFixed(1) + '%' : 'Unknown'}
                </p>
              </div>
            </div>

            {result.risk_factors && result.risk_factors.length > 0 && (
              <div style={{ 
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '16px',
                border: '1px solid #e5e7eb'
              }}>
                <p style={{ 
                  margin: '0 0 12px 0',
                  fontSize: '14px',
                  color: '#6b7280',
                  fontWeight: '500'
                }}>
                  Risk Factors
                </p>
                <ul style={{ 
                  margin: '0',
                  paddingLeft: '0',
                  listStyle: 'none'
                }}>
                  {result.risk_factors.map((factor: string, index: number) => (
                    <li key={index} style={{ 
                      marginBottom: '4px',
                      color: '#374151',
                      fontSize: '14px',
                      paddingLeft: '12px',
                      position: 'relative'
                    }}>
                      <span style={{
                        position: 'absolute',
                        left: '2px',
                        color: '#374151'
                      }}>•</span>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App