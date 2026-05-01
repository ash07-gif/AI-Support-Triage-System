Multi-Domain Support Triage Agent

This project is a **rule-driven AI triage system** designed to process support tickets across different ecosystems (HackerRank, Claude, Visa) and decide **when to respond vs when to escalate**.

Instead of relying entirely on AI, the system intentionally separates:

* **decision-making (rules)**
* **response generation (LLM)**

to ensure safety and consistency.


What the system actually does

Given a support ticket, it:

1. Classifies the request (bug / feature / product issue / invalid)
2. Estimates risk (low / medium / high)
3. Decides whether to:

   * respond directly
   * escalate to human support
4. Generates a **safe, non-assumptive response**
5. Logs the reasoning behind every decision



Design Philosophy (important)

Most naive solutions try to solve everything using AI.

This system **does not**.

Instead:

* **Rules handle critical decisions** → predictable, safe
* **AI handles language only** → flexible but controlled

This avoids:

* hallucinated actions
* unsafe automation (e.g., account restoration claims)
* inconsistent escalation behavior

---

System Flow

```id="flowx1"
Ticket → Classification → Risk → Decision → Response → Output + Logs
```



How decisions are made

1. Classification (rule-based)

Keyword heuristics are used to map tickets into:

* `bug`
* `feature_request`
* `product_issue`
* `invalid`

Reason:

> deterministic behavior is preferred over model variability



2. Risk detection (heuristic scoring)

* High → fraud, unauthorized activity
* Medium → account access, permissions
* Low → general issues

This step is critical because it directly controls escalation.



3. Decision engine

Simple but intentional:

* Medium / High risk → **Escalate**
* Low risk → **Reply**

This ensures:

> sensitive operations are never handled automatically



4. Response generation (LLM)

Used only for:

* phrasing
* guidance

Strict constraints:

* no promises
* no system-level claims
* no fabricated actions



5. Product area detection

Issues are mapped into practical buckets like:

* `payments`
* `account_access`
* `permissions`
* `assessments`

This improves interpretability over raw company labels.


6. Explainability layer

Each ticket produces:

* justification
* confidence score
* full decision trace (`log.txt`)

This makes the system **auditable**, not a black box.


How to run

```bash id="runx1"
python main.py
```

Outputs:

* `output.csv`
* `log.txt`


Optional UI

```bash id="runx2"
streamlit run app.py
```

Used only for visualization and debugging.


Output structure

Each ticket returns:

* `status` (replied / escalated)
* `product_area`
* `request_type`
* `response`
* `justification`
* `confidence`


Tradeoffs (intentional)

This system **does not implement retrieval from support corpus**.

Reason:

> prioritizing safety and consistency over potentially hallucinated or mis-grounded responses

Instead:

* responses are conservative
* escalation is preferred for ambiguity


What can be improved

* Add retrieval (RAG) using support docs
* Replace heuristics with hybrid ML + rules
* Improve domain-specific responses


Key takeaway

This is not just a script—it is a **controlled AI system** where:

* decisions are deterministic
* outputs are explainable
* AI is used carefully, not blindly


