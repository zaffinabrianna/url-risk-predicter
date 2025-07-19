from .url_utils import analyze_redirects
from .domain_utils import analyze_domain
from .risk_scorer import calculate_risk_score


def analyze_url(url: str) -> dict:
    redirect_info = analyze_redirects(url)
    domain_info = analyze_domain(url)
    risk_info = calculate_risk_score(url, redirect_info, domain_info)
    return {
        "original_url": url,
        "redirect info": redirect_info,
        "domain analysis": domain_info,
        **risk_info
    }
