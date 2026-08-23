from fastapi import FastAPI, Request
from pydantic import BaseModel,Field
from typing import List
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

import re
import joblib


class EmailRequest(BaseModel):
    email: str = Field(
        ...,
        max_length=50000
    )


class AnalysisResponse(BaseModel):
    classification: str
    confidence: str
    severity: str
    riskScore: str
    reasons: List[str]
    mitre: List[str]
    urls: List[str]
    emails: List[str]
    ips: List[str]
    mlPrediction: str
    mlConfidence: str

app = FastAPI()




@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print(f"ERROR: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing the request."
        }
    )


model = joblib.load("../models/phishing_model.pkl")
vectorizer = joblib.load("../models/tfidf_vectorizer.pkl")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }




def extract_urls(text):
    urls = re.findall(r'https?://[^\s<>"\']+', text)

    return [
        url.rstrip(".,;:!?)]}")
        for url in urls
    ]


def extract_emails(text):
    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}',
        text
    )

    return [
        email.rstrip(".,;:!?)]}")
        for email in emails
    ]


def extract_ips(text):
    return re.findall(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        text
    )


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(data: EmailRequest):

    email = data.email.lower()

    if not email.strip():

        return {
            "classification": "No Input",
            "confidence": "0%",
            "severity": "None",
            "riskScore": "0/10",
            "reasons": [
                "Please enter an email before analyzing."
            ],
            "mitre": [],
            "urls": [],
            "emails": [],
            "ips": [],
            "mlPrediction": "Not analyzed",
            "mlConfidence": "0%"
        }


    urls = extract_urls(email)

    email_addresses = extract_emails(email)

    ips = extract_ips(email)


    email_tfidf = vectorizer.transform([email])

    ml_prediction = model.predict(email_tfidf)[0]

    ml_probabilities = model.predict_proba(
        email_tfidf
    )[0]

    phishing_probability = ml_probabilities[1]

    ml_confidence = round(
        phishing_probability * 100,
        2
    )


    reasons = []

    risk_score = 1

    classification = "Safe"

    confidence = "99%"

    severity = "Low"


    phishing_keywords = [

        "urgent",
        "verify",
        "click",
        "password",
        "suspended",
        "bank",
        "account",
        "login",
        "confirm",
        "security",
        "immediately"

    ]


    detected_keywords = []

    for word in phishing_keywords:

        if word in email:

            detected_keywords.append(word)


    if len(detected_keywords) > 0:

        keyword_risk = min(
            len(detected_keywords),
            3
        )

        risk_score += keyword_risk

        reasons.append(
            "Suspicious keywords detected: "
            + ", ".join(detected_keywords)
        )


    if len(urls) > 0:

        reasons.append(
            f"Suspicious URL detected "
            f"({len(urls)} URL(s))"
        )

        risk_score += 3


    if len(email_addresses) > 0:

        reasons.append(
            "Email address found"
        )


    if len(ips) > 0:

        reasons.append(
            "IP address found"
        )

        risk_score += 1


    advanced_indicators = []


    urgency_pattern = (
        r"\b("
        r"urgent|"
        r"immediately|"
        r"act now|"
        r"right away|"
        r"as soon as possible"
        r")\b"
    )

    threat_pattern = (
        r"\b("
        r"suspended|"
        r"locked|"
        r"blocked|"
        r"terminated|"
        r"disabled|"
        r"closed"
        r")\b"
    )

    if (
        re.search(
            urgency_pattern,
            email,
            re.IGNORECASE
        )
        and
        re.search(
            threat_pattern,
            email,
            re.IGNORECASE
        )
    ):

        advanced_indicators.append(
            "Urgency combined with account threat"
        )

        risk_score += 1


    credential_pattern = (
        r"\b("
        r"password|"
        r"passcode|"
        r"login credentials|"
        r"username|"
        r"pin|"
        r"otp"
        r")\b"
    )

    credential_action_pattern = (
        r"\b("
        r"enter|"
        r"provide|"
        r"confirm|"
        r"verify|"
        r"submit|"
        r"reset"
        r")\b"
    )

    if (
        re.search(
            credential_pattern,
            email,
            re.IGNORECASE
        )
        and
        re.search(
            credential_action_pattern,
            email,
            re.IGNORECASE
        )
    ):

        advanced_indicators.append(
            "Possible credential harvesting attempt"
        )

        risk_score += 1


    deadline_pattern = (
        r"\b("
        r"within\s+\d+\s+"
        r"(hour|hours|minute|minutes|day|days)"
        r"|act now"
        r"|immediately"
        r"|limited time"
        r")\b"
    )

    if re.search(
        deadline_pattern,
        email,
        re.IGNORECASE
    ):

        advanced_indicators.append(
            "Time-pressure or deadline language detected"
        )

        risk_score += 1


    financial_pattern = (
        r"\b("
        r"bank|"
        r"banking|"
        r"payment|"
        r"credit card|"
        r"debit card|"
        r"account balance|"
        r"transaction"
        r")\b"
    )

    if re.search(
        financial_pattern,
        email,
        re.IGNORECASE
    ):

        advanced_indicators.append(
            "Financial or account targeting detected"
        )

        risk_score += 1


    impersonation_pattern = (
        r"\b("
        r"security department|"
        r"security team|"
        r"IT department|"
        r"IT support|"
        r"technical support|"
        r"account department"
        r")\b"
    )

    if re.search(
        impersonation_pattern,
        email,
        re.IGNORECASE
    ):

        advanced_indicators.append(
            "Possible trusted-organization impersonation"
        )

        risk_score += 1


    reasons.extend(
        advanced_indicators
    )


    if ml_prediction == 1:

        reasons.append(
            f"ML model detected phishing "
            f"({ml_confidence}% confidence)"
        )

        if phishing_probability >= 0.90:

            risk_score += 4

        elif phishing_probability >= 0.70:

            risk_score += 3

        elif phishing_probability >= 0.50:

            risk_score += 2


    else:

        reasons.append(
            f"ML model classified email as legitimate "
            f"({100 - ml_confidence:.2f}% confidence)"
        )


    if (
        ml_prediction == 0
        and risk_score >= 6
    ):

        reasons.append(
            "ML prediction conflicts with "
            "rule-based threat indicators"
        )


    elif (
        ml_prediction == 1
        and risk_score <= 3
    ):

        reasons.append(
            "ML prediction indicates phishing "
            "despite limited rule-based indicators"
        )


    if (
        len(detected_keywords) >= 5
        and len(urls) > 0
    ):

        reasons.append(
            "Multiple phishing indicators "
            "combined with a suspicious URL"
        )

        risk_score += 2


    risk_score = min(
        risk_score,
        10
    )


    risk_confidence = risk_score * 10


    if risk_score >= 8:

        classification = "Phishing"

        severity = "High"


        confidence_value = (
            (risk_confidence * 0.60)
            +
            (ml_confidence * 0.40)
        )

        confidence_value = max(
            confidence_value,
            80
        )

        confidence_value = min(
            confidence_value,
            99.99
        )

        confidence = (
            f"{confidence_value:.2f}%"
        )


    elif risk_score >= 4:

        classification = "Suspicious"

        severity = "Medium"


        confidence_value = (
            (risk_confidence * 0.60)
            +
            (ml_confidence * 0.40)
        )

        confidence_value = max(
            confidence_value,
            60
        )

        confidence_value = min(
            confidence_value,
            95
        )

        confidence = (
            f"{confidence_value:.2f}%"
        )


    else:

        classification = "Safe"

        severity = "Low"


        legitimate_confidence = (
            100 - ml_confidence
        )


        confidence_value = (
            (risk_confidence * 0.40)
            +
            (legitimate_confidence * 0.60)
        )

        confidence_value = max(
            confidence_value,
            60
        )

        confidence_value = min(
            confidence_value,
            99.99
        )

        confidence = (
            f"{confidence_value:.2f}%"
        )


    mitre_techniques = []


    if classification in [
        "Phishing",
        "Suspicious"
    ]:

        mitre_techniques.append(
            "T1566 - Phishing"
        )


    if len(urls) > 0:

        mitre_techniques.append(
            "T1566.002 - Spearphishing Link"
        )


    if any(
        "credential harvesting"
        in indicator.lower()
        for indicator in advanced_indicators
    ) and len(urls) > 0:

        mitre_techniques.append(
            "T1056.003 - Web Portal Capture"
        )


    mitre_techniques = list(
        dict.fromkeys(
            mitre_techniques
        )
    )


    return {

        "classification": classification,

        "confidence": confidence,

        "severity": severity,

        "riskScore": f"{risk_score}/10",

        "reasons": reasons,

        "mitre": mitre_techniques,

        "urls": urls,

        "emails": email_addresses,

        "ips": ips,

        "mlPrediction": (
            "Phishing"
            if ml_prediction == 1
            else "Legitimate"
        ),

        "mlConfidence": f"{ml_confidence}%"
    }