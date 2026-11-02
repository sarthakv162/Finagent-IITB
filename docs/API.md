# API Reference

Local development base URL: `http://127.0.0.1:8000`

Interactive OpenAPI documentation: `/docs`

## Health check

`GET /`

Example response:

```json
{
  "status": "ok",
  "message": "FinAgent API is running"
}
```

## Run the browser agent

`POST /run-agent`

### Request body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `goal` | string | Yes | Non-empty natural-language task description. |
| `start_url` | string | Yes | Non-empty page URL. Use the local demo URL. |
| `biller` | string or null | No | Biller name to put in the demo form. |
| `amount` | positive number or null | No | Positive amount to put in the demo form. |
| `headless` | boolean | No | Run browser without a visible window. Defaults to `true`. |
| `auto_confirm` | boolean | No | Permit the confirmation-gated demo click. Defaults to `false`. |

### Example

```bash
curl -X POST "http://127.0.0.1:8000/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Pay electricity bill to Demo Power for 250",
    "start_url": "http://localhost:9000/",
    "biller": "Demo Power",
    "amount": 250,
    "headless": false,
    "auto_confirm": false
  }'
```

### Possible agent statuses

| Status | Meaning |
| --- | --- |
| `needs_input` | A biller or amount could not be resolved. |
| `needs_confirmation` | The safety interceptor paused before the payment click. |
| `needs_correction` | The page showed a message interpreted as an error. |
| `success` | The demo page displayed a success message. |
| `executed_script` | The action sequence completed without a detected success message. |

These statuses describe the local demonstration only. A `success` response means the dummy page displayed a simulated success state; it does not represent a real transaction.

## Safety

Only test against the included dummy website or another local page you control. Do not send real banking credentials or financial information. The current keyword-based confirmation check is a prototype safeguard, not a production-grade authorization boundary.