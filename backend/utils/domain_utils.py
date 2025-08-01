import re
import math
from typing import Dict, Any, List
from .url_utils import extract_domain

# Suspicious TLDs commonly used in phishing
SUSPICIOUS_TLDS = {
    'tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'site', 'online', 'click',
    'link', 'live', 'space', 'website', 'tech', 'digital', 'app', 'web'
}

# Suspicious keywords often found in malicious domains
SUSPICIOUS_KEYWORDS = [
    'secure', 'login', 'verify', 'update', 'confirm', 'account', 'bank',
    'paypal', 'google', 'facebook', 'amazon', 'apple', 'microsoft',
    'netflix', 'spotify', 'dropbox', 'onedrive', 'icloud'
]

# Popular brands for similarity checking
POPULAR_BRANDS = [
    'google', 'facebook', 'amazon', 'apple', 'microsoft', 'netflix',
    'paypal', 'ebay', 'linkedin', 'twitter', 'instagram', 'youtube',
    'dropbox', 'spotify', 'uber', 'airbnb', 'stripe', 'shopify'
]


def analyze_domain(url: str) -> Dict[str, Any]:
    """
    Analyze domain for suspicious characteristics.

    Args:
        url: URL to analyze

    Returns:
        Dictionary with domain analysis results
    """
    domain = extract_domain(url)

    return {
        'domain': domain,
        'suspicious_tld': check_suspicious_tld(domain),
        'suspicious_keywords': check_suspicious_keywords(domain),
        'entropy_score': calculate_entropy(domain),
        'similarity_attacks': detect_similarity_attacks(domain),
        'brand_similarity': check_brand_similarity(domain),
        'domain_age': None,  # Would need WHOIS lookup for real implementation
        'length': len(domain)
    }


def check_suspicious_tld(domain: str) -> bool:
    """Check if domain uses suspicious TLD."""
    tld = domain.split('.')[-1].lower()
    return tld in SUSPICIOUS_TLDS


def check_suspicious_keywords(domain: str) -> List[str]:
    """Check for suspicious keywords in domain."""
    found_keywords = []
    domain_lower = domain.lower()

    # Extract domain name without TLD for brand checking
    domain_name = domain_lower.split('.')[0]

    # Skip keyword detection for legitimate brand domains
    if domain_name in POPULAR_BRANDS:
        return found_keywords

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in domain_lower:
            found_keywords.append(keyword)

    return found_keywords


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of text."""
    if not text:
        return 0.0

    # Count character frequencies
    char_count = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1

    # Calculate entropy
    entropy = 0.0
    length = len(text)

    for count in char_count.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def detect_similarity_attacks(domain: str) -> Dict[str, bool]:
    """Detect various similarity-based attacks."""
    domain_lower = domain.lower()

    return {
        'punycode': detect_punycode(domain),
        'bit_squatting': detect_bit_squatting(domain_lower),
        'combosquatting': detect_combosquatting(domain_lower)
    }


def detect_punycode(domain: str) -> bool:
    """Detect punycode encoding (IDN homograph attacks)."""
    return 'xn--' in domain


def detect_bit_squatting(domain: str) -> bool:
    """Detect bit-squatting attacks (similar domains with bit flips)."""
    # Extract domain name without TLD for brand checking
    domain_name = domain.split('.')[0]

    # Skip for legitimate brand domains
    if domain_name in POPULAR_BRANDS:
        return False

    # This is a simplified version - real implementation would need
    # more sophisticated character similarity analysis
    # Only flag if multiple suspicious chars are present or in suspicious patterns
    suspicious_chars = ['0', '1', 'l', 'i', 'o']
    suspicious_count = sum(1 for char in suspicious_chars if char in domain)

    # Only flag if multiple suspicious chars or specific patterns
    if suspicious_count >= 2:
        return True

    # Check for specific suspicious patterns
    suspicious_patterns = ['go0gle', 'g00gle', 'goog1e', 'g00g1e']
    if any(pattern in domain for pattern in suspicious_patterns):
        return True

    return False


def detect_combosquatting(domain: str) -> bool:
    """Detect combosquatting (combining brand names with other words)."""
    domain_parts = domain.split('.')[0].split('-')

    for brand in POPULAR_BRANDS:
        if brand in domain_parts:
            # Check if there are other parts besides the brand
            other_parts = [part for part in domain_parts if part != brand]
            if other_parts:
                return True

    return False


def check_brand_similarity(domain: str) -> Dict[str, bool]:
    """Check for similarity to popular brands."""
    domain_lower = domain.lower()
    domain_name = domain_lower.split('.')[0]  # Extract domain name without TLD
    similarities = {}

    for brand in POPULAR_BRANDS:
        # Skip if this is the legitimate brand domain
        if domain_name == brand:
            similarities[brand] = False
        # Simple similarity check - could be enhanced with edit distance
        elif brand in domain_lower or domain_lower in brand:
            similarities[brand] = True
        else:
            # Check for common typos or variations
            if len(brand) > 3 and any(brand[i:i+3] in domain_lower for i in range(len(brand)-2)):
                similarities[brand] = True
            else:
                similarities[brand] = False

    return similarities


def get_domain_age(domain: str) -> int:
    """
    Get domain age in days.
    This would require WHOIS lookup in a real implementation.
    """
    # Placeholder - would need to implement WHOIS lookup
    return None


def calculate_domain_reputation(domain: str) -> float:
    """
    Calculate domain reputation score.
    This would integrate with reputation services in a real implementation.
    """
    # Placeholder - would need to integrate with reputation APIs
    return 0.5
