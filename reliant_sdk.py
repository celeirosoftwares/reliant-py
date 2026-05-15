"""
Reliant Python SDK
Official Python SDK for Reliant — LLM Reliability Layer
"""

import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any


class ReliantException(Exception):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class Reliant:
    """Official Python SDK for Reliant — LLM Reliability Layer"""

    def __init__(self, api_key: str, user_id: str, base_url: str = "https://reliant-production.up.railway.app", timeout: int = 120):
        if not api_key:
            raise ReliantException("api_key is required")
        if not user_id:
            raise ReliantException("user_id is required")

        self.api_key = api_key
        self.user_id = user_id
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def execute(self, prompt: str, schema_id: str, provider: str, model: str, max_retries: int = 3) -> Dict[str, Any]:
        """Execute a prompt with schema validation and intelligent retry."""
        return self._request("POST", "/execute", {
            "prompt": prompt,
            "schema_id": schema_id,
            "provider": provider,
            "model": model,
            "user_id": self.user_id,
            "options": {"max_retries": max_retries},
        })

    def list_schemas(self) -> Dict[str, Any]:
        """List all schemas for the project."""
        return self._request("GET", "/schemas")

    def get_schema(self, schema_id: str) -> Dict[str, Any]:
        """Get a schema by ID."""
        return self._request("GET", f"/schemas/{schema_id}")

    def create_schema(self, name: str, slug: str, definition: dict, safe_fallback: Optional[dict] = None, description: Optional[str] = None, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Create a new schema."""
        body: Dict[str, Any] = {
            "name": name,
            "slug": slug,
            "definition": definition,
        }
        if safe_fallback is not None:
            body["safe_fallback"] = safe_fallback
        if description:
            body["description"] = description
        if system_prompt:
            body["system_prompt"] = system_prompt
        return self._request("POST", "/schemas", body)

    def list_executions(self, limit: int = 20, status: Optional[str] = None, schema_id: Optional[str] = None) -> Dict[str, Any]:
        """List executions with optional filters."""
        params = f"?limit={limit}"
        if status:
            params += f"&status={status}"
        if schema_id:
            params += f"&schema_id={schema_id}"
        return self._request("GET", f"/executions{params}")

    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get execution details by ID."""
        return self._request("GET", f"/executions/{execution_id}")

    def get_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Get metrics summary."""
        return self._request("GET", f"/metrics/summary?days={days}")

    def get_metrics_by_schema(self, days: int = 30) -> Dict[str, Any]:
        """Get metrics broken down by schema."""
        return self._request("GET", f"/analytics/by-schema?days={days}")

    def get_metrics_by_provider(self, days: int = 30) -> Dict[str, Any]:
        """Get metrics broken down by provider."""
        return self._request("GET", f"/analytics/by-provider?days={days}")

    def _request(self, method: str, path: str, body: Optional[dict] = None) -> Dict[str, Any]:
        url = self.base_url + path
        data = json.dumps(body).encode("utf-8") if body else None

        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Content-Type": "application/json",
                "X-Reliant-Key": self.api_key,
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode("utf-8"))
                message = error_data.get("message") or error_data.get("error") or str(e)
            except Exception:
                message = str(e)
            raise ReliantException(f"Reliant API error ({e.code}): {message}", e.code)
        except urllib.error.URLError as e:
            raise ReliantException(f"Connection error: {e.reason}")
