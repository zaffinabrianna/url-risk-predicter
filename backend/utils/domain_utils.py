from typing import Dict, Any
import math
from urllib.parse import urlparse


def analyze_domain(url: str) -> Dict[str, Any]:
    """
    Analyze domain for suspicious patterns.

    Args:
        url: The URL to analyze

    Returns:
        Dictionary with domain analysis:
        - domain: The domain name
        - tld: Top-level domain
        - suspicious_tld: Boolean
        - suspicious_keywords: List of suspicious keywords found
        - entropy_score: Domain entropy
        - length: Domain length
    """

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if ':' in domain:
        domain = domain.split(':')[0]

    analysis = {
        "domain": domain,
        "tld": domain.split('.')[-1] if '.' in domain else '',
        "suspicious_tld": False,
        "suspicious_keywords": [],
        "entropy_score": calculate_entropy(domain),
        "length": len(domain),
        "similarity_attacks": detect_similarity_attacks(domain),
        "brand_similarity": check_brand_similarity(domain)
    }

    # add TLD check and keyword check

    return analysis


def calculate_entropy(text: str) -> float:
    """
    Calculate entropy of a domain.
    """
    if not text:
        return 0.0

    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    entropy = 0.0
    length = len(text)
    for count in frequency.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


def detect_similarity_attacks(domain: str) -> Dict[str, bool]:
    """
    Detect various similarity-based attacks from the research paper.
    """
