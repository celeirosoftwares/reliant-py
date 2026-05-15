# reliant-py

SDK oficial Python para o [Reliant](https://reliant.ia.br) — LLM Reliability Layer.

## Instalação

```bash
pip install reliant-py
```

## Início rápido

```python
from reliant import Reliant

client = Reliant(
    api_key="rel_...",    # Dashboard → Configurações
    user_id="seu-user-id", # Dashboard → Configurações
    base_url="https://reliant-production.up.railway.app",
)

# Executar com validação garantida
result = client.execute(
    prompt="Extraia os dados: João Silva, joao@email.com",
    schema_id="id-do-seu-schema",
    provider="anthropic",
    model="claude-sonnet-4-20250514",
)

print(result["output"])   # {"name": "João Silva", "email": "joao@email.com"}
print(result["metadata"]["attempts"])  # 1
print(result["metadata"]["latency_ms"])  # 743
```

## Providers suportados

- `anthropic` — Claude Sonnet, Opus, Haiku
- `openai` — GPT-4o, GPT-4o-mini
- `gemini` — Gemini 1.5 Pro, Flash
- `groq` — Llama 3, Mixtral
- `mistral` — Mistral Large, Small

## Métodos

### execute()

```python
result = client.execute(
    prompt="seu prompt",
    schema_id="sch_...",
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    max_retries=3,
)
# result["success"] → bool
# result["output"]  → dict com o output validado
# result["status"]  → "success" | "fallback" | "failed"
# result["metadata"]["execution_id"]
# result["metadata"]["attempts"]
# result["metadata"]["latency_ms"]
# result["metadata"]["tokens_used"]
```

### list_schemas() / get_schema() / create_schema()

```python
schemas = client.list_schemas()

schema = client.get_schema("id-do-schema")

new_schema = client.create_schema(
    name="Extração de Contato",
    slug="contact-extraction",
    definition={
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
        }
    },
    safe_fallback={"name": None, "email": None},
)
```

### list_executions() / get_execution()

```python
executions = client.list_executions(limit=20, status="failed")
execution = client.get_execution("exec_...")
```

### get_metrics()

```python
metrics = client.get_metrics(days=30)
print(metrics["success_rate"])       # 98.5
print(metrics["total_executions"])   # 1420
print(metrics["estimated_cost_usd"]) # 0.0842
```

## Tratamento de erros

```python
from reliant import Reliant, ReliantException

try:
    result = client.execute(...)
except ReliantException as e:
    print(f"Erro {e.status_code}: {e}")
```

## Requisitos

- Python >= 3.7
- Sem dependências externas
