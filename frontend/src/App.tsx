import { useState } from 'react'
import './App.css'

function processRiskFactors(riskFactors: string[]) {
  if (riskFactors.some(f => f.toLowerCase().includes("brand similarity"))) {
    return [
      ...riskFactors.filter(f => !f.toLowerCase().includes("brand similarity")),
      "Popular brand similarity"
    ];
  }
  return riskFactors;
}

function isValidUrlFormat(str: string) {
  if (str.includes(' ')) return false;
  try {
    // Prepend https:// if missing
    const testStr = str.startsWith('http://') || str.startsWith('https://') ? str : 'https://' + str;
    const url = new URL(testStr);
    // Must be http/https, have at least one dot, and a valid hostname
    return (
      (url.protocol === 'http:' || url.protocol === 'https:') &&
      url.hostname.includes('.') &&
      !url.hostname.startsWith('.') &&
      !url.hostname.endsWith('.')
    );
  } catch {
    return false;
  }
}

function App() {
  const [url, setUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')
  const [feedback, setFeedback] = useState('')
  const [vote, setVote] = useState('')
  const [feedbackStatus, setFeedbackStatus] = useState('')
  const [doNotLog, setDoNotLog] = useState(false)

  const analyzeUrl = async () => {
    setError('');
    setResult(null);
    setFeedback('');
    setVote('');
    setFeedbackStatus('');
    if (!url.trim()) {
      setError('Please enter a URL to analyze.');
      return;
    }
    if (url.includes(' ')) {
      setError('URL cannot contain spaces.');
      return;
    }
    if (!isValidUrlFormat(url.trim())) {
      setError('Please enter a valid URL (e.g., https://example.com).');
      return;
    }
    let urlToAnalyze = url.trim();
    if (!/^https?:\/\//i.test(urlToAnalyze)) {
      urlToAnalyze = 'https://' + urlToAnalyze;
    }
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: urlToAnalyze,
          do_not_log: doNotLog
        })
      });
      let data;
      try {
        data = await response.json();
      } catch {
        setError('An unexpected error occurred. Please try again later.');
        return;
      }
      if (!response.ok) {
        setError(data.detail || 'An unexpected error occurred. Please try again later.');
        return;
      }
      setResult(data);
    } catch (err) {
      setError('Unable to connect to the server. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  }

  const submitFeedback = async () => {
    setFeedbackStatus('');
    if (!vote) {
      setFeedbackStatus('Please select whether the analysis was correct.');
      return;
    }
    if (feedback.length > 500) {
      setFeedbackStatus('Feedback must be 500 characters or less.');
      return;
    }
    if (/<script>/i.test(feedback)) {
      setFeedbackStatus('Feedback cannot contain script tags.');
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          user_vote: vote,
          feedback: feedback,
          do_not_log: doNotLog
        })
      });
      let data;
      try {
        data = await response.json();
      } catch {
        setFeedbackStatus('An unexpected error occurred. Please try again later.');
        return;
      }
      if (!response.ok) {
        setFeedbackStatus(data.detail || 'An unexpected error occurred. Please try again later.');
        return;
      }
      setFeedbackStatus('Thank you for your feedback!');
      setVote('');
      setFeedback('');
    } catch (err) {
      setFeedbackStatus('Unable to connect to the server. Please check your connection and try again.');
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
    <>
      {isLoading && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(255,255,255,0.6)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{
            width: 48,
            height: 48,
            border: '6px solid #e5e7eb',
            borderTop: '6px solid #6366f1',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }} />
          <style>
            {`@keyframes spin { 100% { transform: rotate(360deg); } }`}
          </style>
        </div>
      )}
      <div
        style={{
          maxWidth: '700px',
          margin: '0 auto',
          backgroundColor: 'white',
          borderRadius: '18px',
          boxShadow: '0 8px 32px 0 rgba(31, 41, 55, 0.12)',
          padding: '48px 48px 32px 48px',
          marginTop: '32px',
          marginBottom: '32px',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{
            fontSize: '2.2rem',
            fontWeight: 800,
            color: '#1e293b',
            marginBottom: '10px',
            letterSpacing: '-1px',
          }}>
            LinkShield
          </h1>
          <p style={{
            fontSize: '1.08rem',
            color: '#64748b',
            margin: '0',
            fontWeight: 500,
          }}>
            Smart Malicious URL Checker
          </p>
        </div>

        <div style={{ marginBottom: '28px' }}>
          <div style={{
            display: 'flex',
            gap: '10px',
            marginBottom: '10px',
          }}>
            <input
              type="text"
              placeholder="Enter URL to analyze (e.g., https://example.com)..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{
                flex: 1,
                padding: '14px 18px',
                border: '2px solid #e0e7ef',
                borderRadius: '10px',
                fontSize: '16px',
                outline: 'none',
                transition: 'border-color 0.2s',
                background: '#f1f5f9',
                fontWeight: 500,
              }}
              onFocus={(e) => e.target.style.borderColor = '#6366f1'}
              onBlur={(e) => e.target.style.borderColor = '#e0e7ef'}
            />
            <button
              onClick={analyzeUrl}
              disabled={isLoading || !url}
              style={{
                padding: '14px 28px',
                background: isLoading || !url ? '#cbd5e1' : 'linear-gradient(90deg, #6366f1 0%, #3b82f6 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '10px',
                fontSize: '16px',
                fontWeight: 700,
                cursor: isLoading || !url ? 'not-allowed' : 'pointer',
                boxShadow: isLoading || !url ? 'none' : '0 2px 8px 0 rgba(59, 130, 246, 0.08)',
                transition: 'background 0.2s',
              }}
            >
              {isLoading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', marginTop: '8px', marginBottom: '18px' }}>
            <input
              type="checkbox"
              id="doNotLog"
              checked={doNotLog}
              onChange={e => setDoNotLog(e.target.checked)}
              style={{ marginRight: '8px' }}
            />
            <label htmlFor="doNotLog" style={{ fontSize: '14px', color: '#6b7280' }}>
              Do not log this analysis (your result and feedback will not be saved)
            </label>
          </div>
        </div>

        {error && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '8px',
            color: '#dc2626',
            marginBottom: '20px',
            textAlign: 'center',
            fontWeight: 500,
          }}>
            {error}
          </div>
        )}

        {result && (
          <div style={{
            backgroundColor: '#f9fafb',
            borderRadius: '14px',
            padding: '28px 20px',
            border: '1px solid #e5e7eb',
            marginBottom: '32px',
            boxShadow: '0 2px 8px 0 rgba(59, 130, 246, 0.04)',
          }}>
            <h2 style={{
              fontSize: '1.3rem',
              fontWeight: 700,
              color: '#1e293b',
              marginBottom: '18px',
              letterSpacing: '-0.5px',
            }}>
              Analysis Results
            </h2>

            <div style={{
              display: 'flex',
              gap: '18px',
              marginBottom: '18px',
              flexWrap: 'wrap',
            }}>
              <div style={{
                flex: 1,
                minWidth: '120px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                background: '#fff',
                borderRadius: '8px',
                border: '1px solid #e5e7eb',
                padding: '18px 0',
                marginBottom: '8px',
              }}>
                <span style={{
                  fontSize: '13px',
                  color: '#64748b',
                  fontWeight: 500,
                  marginBottom: '6px',
                }}>Risk Level</span>
                <span style={{
                  display: 'inline-block',
                  padding: '6px 18px',
                  borderRadius: '999px',
                  background: getRiskColor(result.risk_level) + '22',
                  color: getRiskColor(result.risk_level),
                  fontWeight: 700,
                  fontSize: '1.1rem',
                  letterSpacing: '-0.5px',
                }}>{result.risk_level || 'Unknown'}</span>
              </div>
              <div style={{
                flex: 1,
                minWidth: '120px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                background: '#fff',
                borderRadius: '8px',
                border: '1px solid #e5e7eb',
                padding: '18px 0',
                marginBottom: '8px',
              }}>
                <span style={{
                  fontSize: '13px',
                  color: '#64748b',
                  fontWeight: 500,
                  marginBottom: '6px',
                }}>Risk Score</span>
                <span style={{
                  display: 'inline-block',
                  padding: '6px 18px',
                  borderRadius: '999px',
                  background: '#f1f5f9',
                  color: '#1e293b',
                  fontWeight: 700,
                  fontSize: '1.1rem',
                  letterSpacing: '-0.5px',
                }}>{typeof result.risk_score === 'number' ? (result.risk_score * 100).toFixed(1) + '%' : 'Unknown'}</span>
              </div>
            </div>

            {result.risk_factors && result.risk_factors.length > 0 && (
              <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '16px',
                border: '1px solid #e5e7eb',
                marginBottom: '20px',
              }}>
                <p style={{
                  margin: '0 0 12px 0',
                  fontSize: '14px',
                  color: '#6b7280',
                  fontWeight: '500',
                }}>
                  Risk Factors
                </p>
                <ul style={{
                  margin: '0',
                  paddingLeft: '0',
                  listStyle: 'none',
                }}>
                  {processRiskFactors(result.risk_factors).map((factor: string, index: number) => (
                    <li key={index} style={{
                      marginBottom: '4px',
                      color: '#374151',
                      fontSize: '14px',
                      paddingLeft: '12px',
                      position: 'relative',
                    }}>
                      <span style={{
                        position: 'absolute',
                        left: '2px',
                        color: '#374151',
                      }}>•</span>
                      {factor}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Divider */}
            {!doNotLog && <hr style={{ border: 'none', borderTop: '1px solid #e5e7eb', margin: '28px 0 18px 0' }} />}

            {/* Feedback Section */}
            {!doNotLog && (
              <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '16px',
                border: '1px solid #e5e7eb',
                marginTop: '0',
              }}>
                <p style={{
                  margin: '0 0 12px 0',
                  fontSize: '14px',
                  color: '#6b7280',
                  fontWeight: '500',
                }}>
                  Was this analysis correct?
                </p>
                <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                  <button
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: vote === 'Malicious' ? '2px solid #ef4444' : '1px solid #e5e7eb',
                      backgroundColor: vote === 'Malicious' ? '#fee2e2' : 'white',
                      color: '#ef4444',
                      fontWeight: '600',
                      cursor: 'pointer',
                    }}
                    onClick={() => setVote('Malicious')}
                  >
                    Malicious
                  </button>
                  <button
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: vote === 'Safe' ? '2px solid #10b981' : '1px solid #e5e7eb',
                      backgroundColor: vote === 'Safe' ? '#d1fae5' : 'white',
                      color: '#10b981',
                      fontWeight: '600',
                      cursor: 'pointer',
                    }}
                    onClick={() => setVote('Safe')}
                  >
                    Safe
                  </button>
                  <button
                    style={{
                      padding: '8px 16px',
                      borderRadius: '6px',
                      border: vote === 'Unsure' ? '2px solid #f59e0b' : '1px solid #e5e7eb',
                      backgroundColor: vote === 'Unsure' ? '#fef3c7' : 'white',
                      color: '#f59e0b',
                      fontWeight: '600',
                      cursor: 'pointer',
                    }}
                    onClick={() => setVote('Unsure')}
                  >
                    Unsure
                  </button>
                </div>
                <textarea
                  placeholder="Optional comment..."
                  value={feedback}
                  onChange={e => setFeedback(e.target.value)}
                  style={{
                    width: '100%',
                    minHeight: '48px',
                    borderRadius: '6px',
                    border: '1px solid #e5e7eb',
                    padding: '8px',
                    fontSize: '14px',
                    marginBottom: '12px',
                    resize: 'vertical',
                  }}
                />
                <button
                  onClick={submitFeedback}
                  style={{
                    padding: '10px 24px',
                    backgroundColor: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '15px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    marginBottom: '8px',
                  }}
                >
                  Submit Feedback
                </button>
                {feedbackStatus && (
                  <div style={{ color: feedbackStatus.includes('Thank') ? '#10b981' : '#ef4444', marginTop: '8px', fontSize: '14px' }}>
                    {feedbackStatus}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  )
}

export default App