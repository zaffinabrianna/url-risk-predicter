from url_utils import analyze_redirects
from domain_utils import analyze_domain
from risk_scorer import calculate_risk_score


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


if __name__ == "__main__":
    test_urls = [
        "https://google.com",
        "https://paypa1-secure.xyz",
        "https://bit.ly/3G5F4k9",
        "https://xn--paypal-fake.com"
    ]
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = analyze_url(url)
        print(result)
