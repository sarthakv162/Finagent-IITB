"""Unit tests for action models, safety checks, and DOM distillation."""

from backend.app.agents.safety_interceptor import SafetyInterceptor, SafetyResult
from backend.app.models.schemas import ActionType, WebAction
from backend.app.utils.dom_distiller import distill_dom


def test_sensitive_click_requires_confirmation():
    action = WebAction(
        action_type=ActionType.CLICK,
        target_description="Pay Now",
        confidence=0.9,
    )

    assert SafetyInterceptor().evaluate(action) == SafetyResult.REQUIRES_CONFIRMATION


def test_non_sensitive_click_is_allowed():
    action = WebAction(
        action_type=ActionType.CLICK,
        target_description="Open profile",
        confidence=0.8,
    )

    assert SafetyInterceptor().evaluate(action) == SafetyResult.SAFE


def test_dom_distiller_extracts_labeled_inputs_and_actions():
    html = """
    <html><head><script>ignored()</script></head><body>
      <label for="amount">Amount</label>
      <input id="amount" type="number" placeholder="Enter amount">
      <button>Pay Now</button>
      <a href="/help">Help</a>
      <p class="success-msg">Payment successful</p>
    </body></html>
    """

    state = distill_dom(html)

    assert state["inputs"] == [
        {"type": "number", "placeholder": "Enter amount", "label": "Amount"}
    ]
    assert state["buttons"] == [{"role": "button", "text": "Pay Now"}]
    assert state["links"] == [{"text": "Help", "href": "/help"}]
    assert state["messages"][0]["kind"] == "success"
    assert "ignored" not in str(state)