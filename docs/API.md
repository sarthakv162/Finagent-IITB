# FinAgent API Reference

Base URL: `http://127.0.0.1:8000`

Interactive documentation: [Swagger UI](http://127.0.0.1:8000/docs)

## Health check

`GET /`

Returns the API service status.

```json
{
  "status": "ok",
  "message": "FinAgent API is running"
}
```

## Execute a browser task

`POST /run-agent`

Submits a natural-language goal and starts a browser-agent run.

### Request fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `goal` | string | Yes | Natural-language task to perform. |
| `start_url` | string | Yes | URL of the page to open. |
| `biller` | string or null | No | Biller name for the banking workflow. |
| `amount` | positive number or null | No | Amount for the banking workflow. |
| `headless` | boolean | No | Run the browser without a visible window. Default: `true`. |
| `auto_confirm` | boolean | No | Allow confirmation-gated actions to proceed. Default: `false`. |

### Example request

```bash
curl -X POST "http://127.0.0.1:8000/run-agent" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Pay electricity bill to Demo Power for 250",
    "start_url": "http://127.0.0.1:9000/",
    "biller": "Demo Power",
    "amount": 250,
    "headless": false,
    "auto_confirm": false
  }'
```

### Response statuses

| Status | Description |
| --- | --- |
| `needs_input` | Additional task details are required. |
| `needs_confirmation` | The agent is waiting for confirmation before proceeding. |
| `needs_correction` | The current page state requires correction. |
| `success` | The requested workflow reached its success state. |
| `executed_script` | The planned browser action sequence was executed. |

## Browser configuration

Use `headless: false` to watch the browser while a task runs. Use `headless: true` for background execution.

## Interactive documentation

FastAPI automatically publishes the complete request schema and endpoint documentation at `/docs` and `/openapi.json`.