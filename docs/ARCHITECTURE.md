# Architecture

FinAgent is organized as a FastAPI service, an asynchronous Playwright execution layer, and a local demo website.

## Runtime flow

1. A client sends a task to `POST /run-agent`.
2. FastAPI validates the payload with the `RunAgentRequest` Pydantic model.
3. The route constructs a `Planner`, `SafetyInterceptor`, `WebExecutor`, and `WebActionAgent`.
4. The agent starts Playwright and navigates to the supplied URL.
5. The observer reads page HTML and passes it through `distill_dom`.
6. The demo implementation resolves the biller and amount, then builds a fixed sequence: type biller, type amount, and click Pay Now.
7. The safety interceptor marks the payment click as requiring confirmation. Without confirmation, the agent returns `needs_confirmation` before executing the click.
8. The browser is closed when the run completes.

## Components

| Component | Responsibility |
| --- | --- |
| `app/main.py` | HTTP API, request validation, dependency construction |
| `agents/web_action_agent.py` | Coordinates observation, demo task flow, safety checks, and execution |
| `agents/planner.py` | Planner abstraction; current LLM integration is a stub |
| `agents/safety_interceptor.py` | Keyword-based confirmation gate for selected click actions |
| `agents/web_executor.py` | Browser lifecycle, navigation, and Playwright actions |
| `utils/dom_distiller.py` | Reduces HTML into structured page information |
| `bank_website/` | Local dummy banking interface |

## Implementation boundaries

The high-level planner and deterministic demo workflow are separate. The current end-to-end payment demonstration does not ask the planner to discover every step dynamically: the agent builds a fixed three-action script after extracting required values. The planner's `_call_llm` method is a placeholder.

The safety interceptor checks a small list of keywords in click targets. It is not sufficient to protect real financial workflows. The demo site's success response is simulated in client-side JavaScript.

## Trust boundary

Treat task text, URLs, page content, and browser-visible text as untrusted input. Use only local or explicitly authorized test pages. Never provide real credentials, payment details, or personal information to this prototype.