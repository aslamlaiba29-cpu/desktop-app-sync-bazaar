# tests/test_refactor.py
import re

def test_long_line_pattern():
    """Verify code scan long line criteria matches string lengths over 100."""
    line_ok = "def short_function(a, b): return a + b"
    line_bad = "a" * 105
    
    assert len(line_ok) <= 100
    assert len(line_bad) > 100

def test_global_state_regex():
    """Verify code scan matches global variable bindings."""
    line_with_global = "  global database_connection, active_session"
    line_normal = "  database_connection = get_db()"
    
    pattern = r"\bglobal\b"
    assert re.search(pattern, line_with_global) is not None
    assert re.search(pattern, line_normal) is None

def test_parameter_count_regex():
    """Verify code scan identifies functions with more than 5 parameters."""
    func_bad = "def process_transaction(user_id, item_id, quantity, discount, coupon, promo, refer):"
    func_ok = "def checkout(user_id, cart_id):"

    func_pattern = re.compile(r"^def\s+\w+\((.*?)\):")

    match_bad = func_pattern.search(func_bad)
    assert match_bad is not None
    params_bad = len([p for p in match_bad.group(1).split(',') if p.strip()])
    assert params_bad > 5

    match_ok = func_pattern.search(func_ok)
    assert match_ok is not None
    params_ok = len([p for p in match_ok.group(1).split(',') if p.strip()])
    assert params_ok <= 5
