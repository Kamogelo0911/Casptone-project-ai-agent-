import json
from pathlib import Path
from database import init_db
from security import get_ticket, update_ticket, SecurityDenied

def attempt(label, fn):
    try:
        result = fn()
        return {"test": label, "outcome": "ALLOWED", "detail": str(result)}
    except SecurityDenied as exc:
        return {"test": label, "outcome": "BLOCKED", "detail": str(exc)}

def main():
    init_db(reset=True)
    results = []
    results.append(attempt("Baseline: read another customer's ticket",
                           lambda: get_ticket(2001, secure=False)))
    results.append(attempt("Secured: read another customer's ticket",
                           lambda: get_ticket(2001, secure=True)))
    results.append(attempt("Baseline: close another customer's ticket",
                           lambda: update_ticket(2001, "closed", secure=False)))
    # Reset target ticket state before secured update attempt.
    init_db(reset=True)
    results.append(attempt("Secured: close another customer's ticket",
                           lambda: update_ticket(2001, "closed", secure=True)))
    results.append(attempt("Secured: read own ticket",
                           lambda: get_ticket(1001, secure=True)))
    Path("results").mkdir(exist_ok=True)
    Path("results/security_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    print("\nEXPERIMENT RESULTS (local synthetic database)")
    for item in results:
        print(f"- {item['test']}: {item['outcome']} — {item['detail']}")
    print("\nSaved results to results/security_results.json")
    print("These are deterministic permission tests, not proof that every LLM prompt injection is blocked.")

if __name__ == "__main__":
    main()
