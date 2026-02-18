# restrict-llm
A universal LLM response restriction proxy and guardrail system.

## Why
Modern LLM APIs are non-deterministic. When your application depends on structured,
predictable output — for DTOs, pipelines, or downstream processing — that's a problem.

restrict-llm sits as an HTTP proxy between your application and any LLM API. It validates
responses against your rules and retries automatically if the model doesn't conform.
No SDK. No language lock-in. Works with any stack.

## How it compares
Libraries like Instructor or Guardrails are Python-specific and require integration into
your codebase. restrict-llm is provider and language agnostic — deploy it once and use
it across any service that can make an HTTP request.

> **Note:** If you're using OpenAI or Gemini with native JSON mode or function calling,
> you may not need this. restrict-llm is most valuable for local models (Ollama, etc.),
> providers without structured output support, or when you need cross-provider consistency.

## Features
- **Provider Agnostic**: Works with any LLM HTTP API (OpenAI, Gemini, Ollama, etc.)
- **Dynamic Configuration**: Define endpoint, headers, and body template per request
- **Validation**: Enforce length, regex, blocked words, and JSON schema
- **Auto-Retry**: Re-prompts the LLM to fix invalid responses up to a configurable limit

## Limitations & Tradeoffs
- **Latency**: Adds a network hop per request. Retries multiply this cost — set
  `retryAttempts` conservatively in latency-sensitive contexts.
- **Retry convergence**: Retrying a non-deterministic model does not guarantee a valid
  response. Always handle the failure case in your application.
- **Security**: API keys are passed in the request body. Do not expose this service
  publicly. Run it within a private network or behind an authenticated gateway.
- **Streaming**: Streaming responses are not currently supported.

## Structure
- `define-restrictllm/api`: API routes and schemas
- `define-restrictllm/core`: Validation and restrictor engine
- `define-restrictllm/services`: Generic LLM HTTP client
- `define-restrictllm/utils`: Helpers and logging

## Installation
```bash
pip install -r requirements.txt
```

## Running
```bash
uvicorn define-restrictllm.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker
```bash
docker build -t restrict-llm .
docker run -p 8000:8000 restrict-llm
```

Or pull directly:
```bash
docker pull riteshm03/restrict-llm
docker run -p 8000:8000 riteshm03/restrict-llm
```

## API Usage
**POST** `/v1/restrictllm/generate`

### Request
```json
{
  "llm": {
    "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "bodyTemplate": {
      "contents": [{"parts": [{"text": "{{prompt}}"}]}]
    },
    "responsePath": "candidates[0].content.parts[0].text"
  },
  "prompt": "Explain Quantum Physics",
  "rules": {
    "maxLength": 200,
    "blockedWords": ["magic"],
    "retryAttempts": 3
  }
}
```

### Response
On success, returns the validated LLM response. On failure after all retry attempts,
returns an error with the last received response and the validation failure reason —
handle this explicitly in your application.

## Security Recommendations
- Deploy behind an API gateway or internal network only
- Do not commit API keys — pass them at runtime via environment variables or secrets management
- Add authentication middleware before exposing to any multi-tenant environment

## Roadmap
- [ ] Streaming support
- [ ] Response caching
- [ ] Metrics and observability hooks
- [ ] Auth middleware
