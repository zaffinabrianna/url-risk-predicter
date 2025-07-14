from typing import Dict, Any
import math
import difflib
from urllib.parse import urlparse


SUSPICIOUS_TLDS = ['.xyz', '.top', '.tk',
                   '.ml', '.ga', '.cf', '.gq', '.zip', '.mov']
SUSPICIOUS_KEYWORDS = [
    'secure', 'login', 'signin', 'account', 'verify', 'confirm',
    'update', 'bank', 'paypal', 'amazon', 'google', 'facebook',
    'microsoft', 'apple', 'netflix', 'spotify', 'ebay', 'pay'
]
KNOWN_BRANDS = [
    'paypal', 'google', 'facebook', 'amazon', 'microsoft',
    'apple', 'netflix', 'spotify', 'ebay', 'yahoo', 'twitter'
]
BIT_SQUAT_CHARS = ['1', '0', '5', '3', '8']
ZERO_WIDTH_CHARS = ['\u200b', '\u200c', '\u200d', '\u2060']


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
    parsed = urlparse(url)
    domain = parsed.netloc.split(':')[0]
    domain_lower = domain.lower().strip()

    analysis = {
        "domain": domain_lower,
        "tld": domain_lower.split('.')[-1] if '.' in domain_lower else '',
        "suspicious_tld": any(domain_lower.endswith(tld) for tld in SUSPICIOUS_TLDS),
        "entropy_score": calculate_entropy(domain_lower),
        "length": len(domain_lower),
        "similarity_attacks": detect_similarity_attacks(domain_lower),
        "brand_similarity": check_brand_similarity(domain_lower)
    }

    suspicious = []
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in domain_lower:
            if kw in KNOWN_BRANDS:
                # only flag brand if it's NOT exactly kw.com
                if domain_lower != f"{kw}.com":
                    suspicious.append(kw)
            else:
                suspicious.append(kw)
    analysis["suspicious_keywords"] = suspicious

    return analysis


def calculate_entropy(domain: str) -> float:
    """
    Calculate entropy of a domain.
    """
    if not domain:
        return 0.0

    freq = {}
    for c in domain:
        freq[c] = freq.get(c, 0) + 1

    entropy = 0.0
    for count in freq.values():
        p = count / len(domain)
        entropy -= p * math.log2(p)
    return entropy


def detect_similarity_attacks(domain: str) -> Dict[str, bool]:
    """
    Detect various similarity-based attacks.
    """
    attacks = {
        "homograph": any(ord(c) > 127 for c in domain),
        "punycode": domain.startswith("xn--"),
        "bit_squatting": any(ch in domain for ch in BIT_SQUAT_CHARS),
        "combosquatting": '-' in domain,
        "zero_width": any(ch in domain for ch in ZERO_WIDTH_CHARS),
    }

    return attacks


def check_brand_similarity(domain: str) -> Dict[str, bool]:
    """
    Check similarity to known brands (inspired by the research paper's USI).
    """
    similarities = {}
    for brand in KNOWN_BRANDS:
        if brand in domain:
            similarities[brand] = True
        else:
            similarities[brand] = calculate_string_similarity(
                domain, brand) > 0.7
    return similarities


def calculate_string_similarity(str1: str, str2: str) -> float:
    return difflib.SequenceMatcher(None, str1, str2).ratio()
