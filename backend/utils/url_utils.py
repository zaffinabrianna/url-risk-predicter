import requests
from urllib.parse import urlparse, urljoin
from typing import Dict, Any, List
import re


def analyze_redirects(url: str) -> Dict[str, Any]:
    """
    Analyze URL redirects to detect potential malicious behavior.

    Args:
        url: URL to analyze

    Returns:
        Dictionary with redirect analysis results
    """
    try:
        # Follow redirects and collect information
        response = requests.get(url, allow_redirects=True, timeout=10)
        history = response.history

        redirect_chain = []
        for resp in history:
            redirect_chain.append({
                'status_code': resp.status_code,
                'url': resp.url,
                'headers': dict(resp.headers)
            })

        # Add final response
        redirect_chain.append({
            'status_code': response.status_code,
            'url': response.url,
            'headers': dict(response.headers)
        })

        return {
            'num_redirects': len(history),
            'redirect_chain': redirect_chain,
            'final_url': response.url,
            'status_code': response.status_code,
            'has_redirects': len(history) > 0
        }

    except Exception as e:
        return {
            'num_redirects': 0,
            'redirect_chain': [],
            'final_url': url,
            'status_code': None,
            'has_redirects': False,
            'error': str(e)
        }


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return url.lower()


def is_valid_url(url: str) -> bool:
    """Check if URL format is valid."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False


def get_url_length_score(url: str) -> float:
    """Calculate URL length suspiciousness score."""
    # Remove protocol for length calculation
    clean_url = url.split('://', 1)[-1] if '://' in url else url

    if len(clean_url) > 150:
        return 1.0
    elif len(clean_url) > 100:
        return 0.7
    elif len(clean_url) > 50:
        return 0.3
    else:
        return 0.0


def detect_suspicious_patterns(url: str) -> List[str]:
    """Detect suspicious patterns in URL."""
    patterns = []
    url_lower = url.lower()

    # Common phishing patterns
    suspicious_patterns = [
        r'login[.-]?secure',
        r'verify[.-]?account',
        r'update[.-]?info',
        r'confirm[.-]?details',
        r'secure[.-]?login',
        r'account[.-]?verify',
        r'bank[.-]?login',
        r'paypal[.-]?secure',
        r'google[.-]?login',
        r'facebook[.-]?login'
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, url_lower):
            patterns.append(f"Suspicious pattern: {pattern}")

    return patterns
