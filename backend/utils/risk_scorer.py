from typing import Dict, Any


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
    risk_score = 0.0
    risk_factors = []

    # 1. Redirect-based risk
    if redirect_info["num_redirects"] > 5:
        risk_score += 0.3
        risk_factors.append("High redirect count (>5)")
    elif redirect_info["num_redirects"] > 2:
        risk_score += 0.15
        risk_factors.append("Multiple redirects (>2)")
