from fastapi import FastAPI
from pydantic import BaseModel

from engine.url_check import url_check
from engine.domain_intel import domain_intel
from engine.link_intel import check_link_intel
from engine.risk_engine import calculate_risk

app = FastAPI(title="PhishGuard API", version="0.1.0")


class URLRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"status": "PhishGuard API running"}


@app.post("/api/check-url")
def check_url(data: URLRequest):
    url = data.url

    base_score, _ = url_check(url)
    domain_score, _, _ = domain_intel(url)
    link_score, _ = check_link_intel(url)

    intel_score = int(domain_score) + int(link_score)

    risk = calculate_risk(
        rule_score=int(base_score),
        ai_confidence=0.0,
        intel_score=intel_score
    )

    # ✅ FLAT RESPONSE (EXTENSION NEEDS THIS)
    return {
        "label": risk["label"],
        "score": risk["score"]
    }
