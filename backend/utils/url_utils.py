from typing import Dict, List, Any
import requests
from urllib.parse import urljoin


def analyze_redirects(url: str) -> Dict[str, Any]:
    """
    Analyze URL redirects and return detailed information.

    Args:
        url: The URL to analyze

    Returns:
        Dictionary with redirect information:
        - redirect_chain: List of all URLs in the chain
        - num_redirects: Number of redirects
        - is_redirect: Boolean indicating if redirects occurred
        - resolved_url: Final URL after all redirects
    """
    redirect_chain = []
    current_url = url
    max_redirects = 10

    try:
        for _ in range(max_redirects):
            response = requests.head(
                current_url,
                allow_redirects=False,
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            redirect_chain.append(current_url)

            # Check if response is a redirect
            if response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location')
                if location:
                    # Convert relative URLs to absolute
                    current_url = urljoin(current_url, location)
                else:
                    break
            else:
                break

    except requests.exceptions.RequestException as e:
        # Handle network errors (timeout, connection refused, etc.)
        return {
            "error": f"Network error: {str(e)}",
            "redirect_chain": [url],
            "num_redirects": 0,
            "is_redirect": False,
            "resolved_url": url
        }
    except Exception as e:
        # Handle other errors
        return {
            "error": f"Unexpected error: {str(e)}",
            "redirect_chain": [url],
            "num_redirects": 0,
            "is_redirect": False,
            "resolved_url": url
        }

    return {
        "redirect_chain": redirect_chain,
        "num_redirects": len(redirect_chain) - 1,
        "is_redirect": len(redirect_chain) > 1,
        "resolved_url": current_url
    }
