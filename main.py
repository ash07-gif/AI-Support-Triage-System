import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- LOAD DATA ----
df = pd.read_csv("support_tickets.csv")
df.columns = df.columns.str.lower().str.strip()

# ---- CLASSIFICATION ----
def classify_request(issue):
    issue = issue.lower()

    if any(word in issue for word in ["bug", "error", "crash"]):
        return "bug"
    
    elif any(word in issue for word in ["feature", "add"]):
        return "feature_request"
    
    elif any(word in issue for word in [
        "payment", "billing", "account", "login",
        "access", "workspace", "permission", "admin"
    ]):
        return "product_issue"
    
    else:
        return "invalid"

# ---- RISK DETECTION ----
def assess_risk(issue):
    issue = issue.lower()

    if any(word in issue for word in [
        "fraud", "unauthorized", "stolen", "scam"
    ]):
        return "high"
    
    elif any(word in issue for word in [
        "access", "account", "login", "permission", "admin"
    ]):
        return "medium"
    
    else:
        return "low"

# ---- DECISION ----
def decide_action(risk, request_type):
    if risk in ["high", "medium"]:
        return "escalated"
    return "replied"

# ---- PRODUCT AREA DETECTION ----
def detect_product_area(issue, company):
    issue = issue.lower()

    if "payment" in issue or "billing" in issue:
        return "payments"
    elif "account" in issue or "login" in issue:
        return "account_access"
    elif "workspace" in issue or "permission" in issue or "admin" in issue:
        return "permissions"
    elif "test" in issue or "assessment" in issue:
        return "assessments"
    elif company:
        return company.lower()
    return "general"

# ---- CONFIDENCE SCORE ----
def confidence_score(risk, request_type):
    if risk == "high":
        return "low"
    elif request_type == "invalid":
        return "low"
    elif risk == "medium":
        return "medium"
    else:
        return "high"

# ---- RESPONSE GENERATION ----
def generate_response(issue, company):
    prompt = f"""
You are a support triage assistant.

Provide safe and helpful guidance only.

Rules:
- Do NOT assume actions (no "we fixed it")
- Do NOT promise access, refunds, or system changes
- Suggest next steps where possible

User issue:
{issue}

Company: {company}

Respond professionally and clearly.
"""

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return response.choices[0].message.content

# ---- PROCESS ALL TICKETS ----
results = []

for _, row in df.iterrows():
    issue = str(row.get("issue", "")).strip()
    company = str(row.get("company", "")).strip()

    if issue == "" or issue.lower() == "nan":
        continue

    request_type = classify_request(issue)
    risk = assess_risk(issue)
    status = decide_action(risk, request_type)

    # ---- INVALID ----
    if request_type == "invalid":
        status = "replied"
        response = "I'm not able to fully understand this request. Could you please provide more details or clarify your issue?"
        justification = "Decision=replied. The issue could not be clearly classified into a supported category."

    # ---- ESCALATED ----
    elif status == "escalated":
        response = "This request involves sensitive account access, permissions, or critical operations. For security reasons, it must be handled by an authorized administrator or official support team."

        justification = f"Decision=escalated. The issue was classified as {request_type} with {risk}-risk indicators requiring human intervention."

    # ---- PRODUCT ISSUE ----
    elif request_type == "product_issue":
        response = "This appears to be a product-related issue. Please refer to the official support resources or contact the support team for further assistance."

        justification = f"Decision=replied. The issue is a product-related query with {risk}-risk level that does not require escalation."

    # ---- OTHER CASES ----
    else:
        try:
            response = generate_response(issue, company)
        except Exception:
            response = "I'm unable to process this request right now. Please contact support."

        if not response or str(response).strip().lower() == "nan":
            response = "I'm unable to provide a complete answer based on the available information. Please contact support for further assistance."

        justification = f"Decision=replied. The issue is classified as {request_type} with {risk}-risk level and is safe for automated handling."

    product_area = detect_product_area(issue, company)
    confidence = confidence_score(risk, request_type)

    # ---- LOGGING ----
    with open("log.txt", "a") as f:
        f.write("----- NEW TICKET -----\n")
        f.write(f"Issue: {issue}\n")
        f.write(f"Company: {company}\n")
        f.write(f"Request Type: {request_type}\n")
        f.write(f"Risk: {risk}\n")
        f.write(f"Decision: {status}\n")
        f.write(f"Product Area: {product_area}\n")
        f.write(f"Confidence: {confidence}\n")
        f.write(f"Justification: {justification}\n\n")

    results.append({
        "status": status,
        "product_area": product_area,
        "response": response,
        "justification": justification,
        "request_type": request_type,
        "confidence": confidence
    })

# ---- SAVE OUTPUT ----
output_df = pd.DataFrame(results)
output_df.to_csv("output.csv", index=False)

print("✅ Done! Output saved to output.csv")