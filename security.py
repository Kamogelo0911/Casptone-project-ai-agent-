from database import connect
from config import CURRENT_CUSTOMER_ID

ALLOWED_STATUSES = {"open", "closed"}

class SecurityDenied(Exception):
    pass

def get_ticket(ticket_id, secure=True):
    # Validate types before querying. Parameterised SQL prevents SQL injection.
    if not isinstance(ticket_id, int):
        raise SecurityDenied("Ticket ID must be an integer.")
    with connect() as conn:
        if secure:
            row = conn.execute(
                "SELECT id, customer_id, subject, body, status FROM tickets WHERE id=? AND customer_id=?",
                (ticket_id, CURRENT_CUSTOMER_ID),
            ).fetchone()
        else:
            # Deliberately vulnerable baseline for a local, synthetic-data comparison only.
            row = conn.execute(
                "SELECT id, customer_id, subject, body, status FROM tickets WHERE id=?",
                (ticket_id,),
            ).fetchone()
    if row is None:
        raise SecurityDenied("Access denied or ticket not found.")
    return dict(row)

def update_ticket(ticket_id, new_status, secure=True):
    if not isinstance(ticket_id, int):
        raise SecurityDenied("Ticket ID must be an integer.")
    if new_status not in ALLOWED_STATUSES:
        raise SecurityDenied("Status must be 'open' or 'closed'.")
    with connect() as conn:
        if secure:
            cursor = conn.execute(
                "UPDATE tickets SET status=? WHERE id=? AND customer_id=?",
                (new_status, ticket_id, CURRENT_CUSTOMER_ID),
            )
        else:
            # Deliberately vulnerable baseline for a local, synthetic-data comparison only.
            cursor = conn.execute(
                "UPDATE tickets SET status=? WHERE id=?",
                (new_status, ticket_id),
            )
        if cursor.rowcount != 1:
            raise SecurityDenied("Access denied or ticket not found.")
    return {"ok": True, "ticket_id": ticket_id, "status": new_status}

def get_synthetic_secret(customer_id, secure=True):
    # Demonstrates that secrets are not exposed by any agent tool.
    if secure:
        raise SecurityDenied("This agent has no tool for retrieving customer secrets.")
    with connect() as conn:
        row = conn.execute(
            "SELECT synthetic_secret FROM customers WHERE id=?", (customer_id,)
        ).fetchone()
    if row is None:
        raise SecurityDenied("Customer not found.")
    return row["synthetic_secret"]
