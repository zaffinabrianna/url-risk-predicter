from typing import Dict, Any

REDIRECT_THRESHOLDS = {
    "high": (5, 0.3),
    "medium": (2, 0.15),
}

WEIGHTS = {
    "suspicious_tld": 0.25,
    "keywords": 0.2,
    "entropy": (4.0, 0.15),  # (threshold, weight)
    "punycode": 0.3,
    "bit_squatting": 0.25,
    "combosquatting": 0.2,
    "brand_similarity": 0.3,
    "long_url": (100, 0.1),  # (length, weight)
    "young_domain": (30, 0.2),  # (days, weight)
}


def calculate_risk_score(url: str, redirect_info: dict, domain_analysis: dict) -> dict:
    """
    Calculate risk score based on multiple factors.

    Args:
        url: Original URL
        redirect_info: Results from analyze_redirects()
        domain_analysis: Results from analyze_domain()

    Returns:
        Dictionary with risk score and breakdown
    """
    score = 0.0
    factors = []

    # Redirects
    num = redirect_info.get("num_redirects", 0)
    for level, (thresh, weight) in REDIRECT_THRESHOLDS.items():
        if num > thresh:
            score += weight
            factors.append(f"{level.capitalize()} redirect count (>{thresh})")
            break

    # Domain flags
    if domain_analysis.get("suspicious_tld"):
        score += WEIGHTS["suspicious_tld"]
        factors.append("Suspicious TLD")

    kw = domain_analysis.get("suspicious_keywords", [])
    if kw:
        score += WEIGHTS["keywords"]
        factors.append(f"Suspicious keywords: {', '.join(kw)}")

    if domain_analysis.get("entropy_score", 0) > WEIGHTS["entropy"][0]:
        score += WEIGHTS["entropy"][1]
        factors.append("High entropy")

    # Similarity
    sim = domain_analysis.get("similarity_attacks", {})
    for attack in ("punycode", "bit_squatting", "combosquatting"):
        if sim.get(attack):
            score += WEIGHTS[attack]
            factors.append(f"{attack.replace('_', ' ').title()} detected")

    # Brand
    brands = [b for b, v in domain_analysis.get(
        "brand_similarity", {}).items() if v]
    if brands:
        score += WEIGHTS["brand_similarity"]
        factors.append(f"Brand similarity: {', '.join(brands)}")

    # URL length
    base = url.split("://", 1)[-1]
    if len(base) > WEIGHTS["long_url"][0]:
        score += WEIGHTS["long_url"][1]
        factors.append("Excessive URL length")

    # Domain age
    age = domain_analysis.get("domain_age")
    if age is not None and age < WEIGHTS["young_domain"][0]:
        score += WEIGHTS["young_domain"][1]
        factors.append("Very new domain")

    score = min(score, 1.0)

    # Level Assignment
    if score >= 0.8:
        level = "High Risk"
    elif score >= 0.5:
        level = "Medium Risk"
    elif score >= 0.3:
        level = "Low Risk"
    else:
        level = "Safe"

    confidence = "high" if len(factors) > 2 else "medium"
    return {"risk_score": score, "risk_level": level, "risk_factors": factors, "confidence": confidence}
