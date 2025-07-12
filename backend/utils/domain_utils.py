from typing import Dict, Any
import math
import difflib
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


def calculate_entropy(domain: str) -> float:
    """
    Calculate entropy of a domain.
    """
    if not domain:
        return 0.0

    frequency = {}
    for char in domain:
        frequency[char] = frequency.get(char, 0) + 1

    entropy = 0.0
    length = len(domain)
    for count in frequency.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


def detect_similarity_attacks(domain: str) -> Dict[str, bool]:
    """
    Detect various similarity-based attacks.
    """
    attacks = {
        "homograph": False,
        "punycode": False,
        "bit_squatting": False,
        "combosquatting": False,
        "zero_width": False
    }

    domain = domain.strip().lower()

    if any(ord(c) > 127 for c in domain):
        attacks["homograph"] = True

    if domain.startswith("xn--"):
        attacks["punycode"] = True

    if any(char in domain for char in ['1', '0', '5', '3', '8']):
        attacks["bit_squatting"] = True

    if '-' in domain:
        attacks["combosquatting"] = True

    # Zero-width character check
    zero_width_chars = ['\u200b', '\u200c', '\u200d', '\u2060']
    if any(char in domain for char in zero_width_chars):
        attacks["zero_width"] = True


def check_brand_similarity(domain: str) -> Dict[str, bool]:
    """
    Check similarity to known brands (inspired by the research paper's USI).
    """
    known_brands = [
        'paypal', 'google', 'facebook', 'amazon', 'microsoft',
        'apple', 'netflix', 'spotify', 'ebay', 'yahoo', 'twitter'
    ]

    domain_lower = domain.lower()
    similarities = {}

    for brand in known_brands:
        if brand in domain_lower:
            similarities[brand] = True
        else:
            score = calculate_string_similarity(domain_lower, brand)
            if score > 0.7:
                similarities[brand] = True

    return similarities


def calculate_string_similarity(str1: str, str2: str) -> float:
    return difflib.SequenceMatcher(None, str1, str2).ratio()
