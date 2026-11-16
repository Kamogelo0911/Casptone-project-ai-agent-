# Security Evaluation of a Tool-Using AI Agent Against Prompt Injection

**Student:** [Your name]  
**Programme / module:** [Complete]  
**Supervisor:** [Complete]  
**Date:** [Complete]

## Abstract
This project develops a local AI customer-support agent and evaluates security risks associated with prompt injection and tool access. The prototype uses Python, an Ollama-hosted language model, and an SQLite database containing synthetic customer and support-ticket records. It compares an intentionally vulnerable baseline with a version that enforces record-level authorisation and input validation in application code. A repeatable test suite measures whether unauthorised record access and ticket updates are allowed or blocked. The project is a controlled educational demonstration and does not use real customer data.

## 1. Introduction
AI agents can do more than generate text: they can select tools and request operations on external data. This increases the impact of prompt injection, where untrusted instructions attempt to change the agent's behaviour. A system prompt is not a reliable security boundary. Tool permissions and data access must be enforced by the application.

## 2. Problem statement
A tool-using AI agent may be persuaded to request operations outside the intended user permissions. If the backend trusts the model's decision without independent checks, a prompt injection may lead to unauthorised data access or changes.

## 3. Aim
To build a local AI agent with SQL database tools and evaluate whether application-enforced security controls reduce unauthorised operations during controlled prompt-injection experiments.

## 4. Objectives
1. Build an AI agent using a local model.
2. Connect the agent to a SQLite database through defined Python tools.
3. Create direct and indirect prompt-injection scenarios using synthetic content.
4. Compare a deliberately vulnerable baseline with a secured implementation.
5. record test outcomes and discuss limitations.

## 5. Technologies
- Python: application logic and security checks.
- Ollama: local language-model runtime.
- SQLite: synthetic customer and ticket data.
- Pytest: repeatable tests.
- JSON: experiment result export.

## 6. Methodology
A prototype was built with two tools: ticket lookup and ticket status update. The sample database contains two fictional customers and tickets. The baseline omits record-level ownership checks; the secured mode filters operations by the fixed application-side customer identity and validates ticket IDs and status values. The identity is not supplied by the model. Tests attempt to read or update a ticket belonging to another synthetic customer, access an authorised ticket, and supply invalid input. The same local environment is used for both modes.

## 7. Test plan
| Test | Expected secured outcome | Evidence |
|---|---|---|
| Read own ticket | Allowed | Returned ticket ID and owner |
| Read another customer's ticket | Blocked | Access-denied result |
| Update another customer's ticket | Blocked | No row updated |
| Invalid status value | Blocked | Validation error |
| Non-integer ticket ID | Blocked | Validation error |
| Direct prompt injection | Must not bypass backend permissions | Model transcript and tool result |
| Indirect injection in ticket content | Must not bypass backend permissions | Model transcript and tool result |

## 8. Results
**Complete this section after running the software. Do not insert hypothetical numbers as actual results.**

- Date and model version tested: [Complete]
- Pytest passed/failed: [Copy actual terminal output]
- Baseline unauthorised read: [Allowed/Blocked, based on run]
- Secured unauthorised read: [Allowed/Blocked, based on run]
- Baseline unauthorised update: [Allowed/Blocked, based on run]
- Secured unauthorised update: [Allowed/Blocked, based on run]
- Direct injection model behaviour: [Observed result]
- Indirect injection model behaviour: [Observed result]

The deterministic security tests evaluate application permissions. Model behaviour may vary and must be recorded separately.

## 9. Discussion
The experiment illustrates why prompt wording alone should not protect sensitive operations. An application-side check can reject access to a record even if the model requests it. The baseline comparison is deliberately simplified and uses synthetic data. It does not represent all real-world agent architectures, and a small test set cannot establish universal resistance to prompt injection.

## 10. Limitations
- Small, synthetic dataset.
- One local model and limited prompt-injection scenarios.
- Model tool-calling behaviour can vary across versions.
- No production authentication, multi-user session management, or external integrations.
- Results do not prove the agent is immune to all prompt injection.

## 11. Conclusion
The project demonstrates a practical method for evaluating prompt injection in a tool-using AI agent. Its main security lesson is that the model should not be trusted to enforce its own permissions. Backend authorisation, input validation, least privilege, and audit logging are necessary safeguards. Future work could add more models, larger test sets, indirect injection through document retrieval, and a more complete evaluation framework.

## References
- OWASP Foundation. *Top 10 for Large Language Model Applications*. https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Ollama. *Ollama Python library*. https://github.com/ollama/ollama-python
- LangChain. *LangGraph SQL agent tutorial*. https://langchain-ai.github.io/langgraph/tutorials/sql-agent/

## Appendix: Reproduction
Follow the setup and test instructions in `README.md`. Include terminal screenshots, test output, and the generated JSON result file in the final submission.
