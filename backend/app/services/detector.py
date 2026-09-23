import re
RULES = [
 ("Urgency",20,"high","Creates time pressure so you act before checking independently.",[r"\burgent\b",r"immediately",r"act now",r"within \d+ (hour|hours|minutes)",r"last chance",r"expires?"]),
 ("Fear / Threat",20,"high","Uses consequences or threats to bypass careful judgment.",[r"account (will be )?(blocked|suspended)",r"legal action",r"\bpolice\b",r"\barrest\b",r"\bpenalty\b",r"\bwarning\b"]),
 ("Authority",15,"medium","Invokes an authority to make the request seem legitimate.",[r"\bbank\b",r"\bgovernment\b",r"\bpolice\b",r"\brbi\b",r"income tax",r"\bofficial\b",r"\bceo\b",r"\bmanager\b"]),
 ("Impersonation",15,"high","Claims to represent a trusted organization; independently verify the sender.",[r"(from|this is|representing) .{0,30}(bank|government|university|delivery|company|employer)",r"customer support",r"security team"]),
 ("Credential Request",25,"high","Requests secrets that legitimate services should not ask for in a message.",[r"\botp\b",r"\bpassword\b",r"\bpin\b",r"\bcvv\b",r"login",r"verification code",r"verify your account"]),
 ("Financial Request",25,"high","Requests payment or transfer before trust has been established.",[r"send money",r"transfer money",r"\bpayment\b",r"\bupi\b",r"bank transfer",r"refund fee",r"processing fee"]),
 ("Suspicious URL",20,"high","Contains a link. Do not open it; verify the destination independently.",[r"https?://\S+",r"\b(bit\.ly|tinyurl\.com|t\.co|goo\.gl)/",r"https?://(?:\d{1,3}\.){3}\d{1,3}",r"\b[a-z0-9-]+\.(xyz|top|click|link|zip)\b"]),
 ("Reward / Prize Manipulation",15,"medium","Uses a prize or reward to create greed and lower skepticism.",[r"\blottery\b",r"\bprize\b",r"\breward\b",r"\bwinner\b",r"\bselected\b",r"claim (your )?(reward|prize)"]),
 ("Emotional Manipulation",10,"medium","Uses emotional pressure or curiosity to influence your decision.",[r"don't tell anyone",r"exclusive",r"secret",r"you won't believe",r"final notice"]),]
def analyze_message(message: str) -> dict:
    text=message.lower().strip(); found=[]; score=100
    for name,penalty,severity,explanation,patterns in RULES:
        evidence=[m.group(0) for p in patterns for m in re.finditer(p,text,re.I)]
        if evidence:
            score-=penalty; found.append({"name":name,"severity":severity,"explanation":explanation,"evidence":list(dict.fromkeys(evidence))[:4]})
    score=max(0,min(100,score)); risk="LOW" if score>=80 else "MEDIUM" if score>=50 else "HIGH"
    explanation=("No common social-engineering indicators were found. This is not proof the message is safe." if not found else "Several high-confidence manipulation signals were detected." if risk=="HIGH" else "The message contains social-engineering indicators that deserve verification.")
    recommendation=("Use normal caution and verify unexpected requests through a trusted channel." if not found else "Do not reply, share data, send money, or open links. Contact the organization through official details." if risk=="HIGH" else "Pause and verify the sender through a trusted channel before taking action.")
    return {"trust_score":score,"risk_level":risk,"detected_techniques":found,"explanation":explanation,"recommendation":recommendation,"nlp_mode":"explainable rule-based NLP fallback"}
