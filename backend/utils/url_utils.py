import requests
from urllib.parse import urljoin
from typing import Dict, List, Any


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
