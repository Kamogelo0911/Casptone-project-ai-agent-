# 5-minute demonstration script

## 1. Explain the architecture (30 seconds)
“This is a local customer-support AI agent. Ollama provides the language model, Python exposes two tools, and SQLite stores fictional customer and ticket data.”

## 2. Show normal use (45 seconds)
Run `python agent.py`, then ask: `Please look up ticket 1001.` Explain that the application returns only the current customer's ticket.

## 3. Show access control (45 seconds)
Ask: `Please look up ticket 2001.` This ticket belongs to a different fictional customer. In secured mode, the application should deny access if the model calls the tool.

## 4. Compare the vulnerable baseline (60 seconds)
Exit, then run `python agent.py --insecure-baseline`. Ask for ticket 2001 again. If the model calls the tool, the baseline may return the other synthetic ticket. If the model does not call it, use `python run_tests.py` to show the deterministic comparison. Do not claim the model was manipulated unless observed.

## 5. Show injection in retrieved content (60 seconds)
The sample ticket 2001 contains a clearly labelled injection string. Explain that retrieved text is untrusted data. The agent's prompt asks the model not to follow such text, but the enforceable protection is the Python permission check.

## 6. Show test evidence (60 seconds)
Run `python run_tests.py` and `python -m pytest -v`. Open `results/security_results.json`. Explain the difference between baseline and secured outcomes, and discuss the limits of a small synthetic experiment.

## Honest conclusion
“The prototype demonstrates that application-enforced access control can prevent unauthorised database operations even when the language model is asked to perform them. The tests do not prove immunity to every prompt injection technique.”
