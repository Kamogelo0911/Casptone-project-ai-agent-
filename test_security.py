import pytest
from database import init_db
from security import get_ticket, update_ticket, SecurityDenied

@pytest.fixture(autouse=True)
def clean_database():
    init_db(reset=True)

def test_own_ticket_is_accessible():
    assert get_ticket(1001, secure=True)["customer_id"] == 101

def test_other_customer_ticket_is_blocked():
    with pytest.raises(SecurityDenied):
        get_ticket(2001, secure=True)

def test_baseline_exposes_other_customer_ticket():
    # This test documents the intentionally vulnerable baseline on synthetic data.
    assert get_ticket(2001, secure=False)["customer_id"] == 202

def test_secure_update_blocks_other_customer():
    with pytest.raises(SecurityDenied):
        update_ticket(2001, "closed", secure=True)

def test_baseline_allows_other_customer_update():
    result = update_ticket(2001, "closed", secure=False)
    assert result["ok"] is True
    assert get_ticket(2001, secure=False)["status"] == "closed"

def test_invalid_status_is_blocked():
    with pytest.raises(SecurityDenied):
        update_ticket(1001, "delete_everything", secure=True)

def test_string_ticket_id_is_blocked():
    with pytest.raises(SecurityDenied):
        get_ticket("1001", secure=True)
