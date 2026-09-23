from app.services.detector import analyze_message

def names(message): return {x["name"] for x in analyze_message(message)["detected_techniques"]}
def test_normal_message_is_low_risk():
    r=analyze_message("Hi, our project meeting is scheduled tomorrow at 10 AM. Please bring your laptop.")
    assert r["risk_level"] == "LOW" and r["trust_score"] >= 80
def test_urgency_bank_scam_is_high_risk():
    r=analyze_message("URGENT! Your bank account will be blocked within 2 hours. Click this link immediately to verify your account.")
    assert r["risk_level"] == "HIGH"; assert {"Urgency","Authority","Fear / Threat","Credential Request"} <= {x["name"] for x in r["detected_techniques"]}
def test_otp_and_financial_scam():
    r=analyze_message("Send your OTP and CVV immediately, then pay the processing fee through UPI.")
    assert {"Credential Request","Financial Request","Urgency"} <= {x["name"] for x in r["detected_techniques"]}
def test_prize_scam(): assert "Reward / Prize Manipulation" in names("Congratulations winner, claim your prize reward immediately")
