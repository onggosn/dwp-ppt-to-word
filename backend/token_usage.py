"""Per-conversion accounting for usage returned by Bedrock."""
from contextvars import ContextVar
from dataclasses import dataclass, field
from functools import wraps
import json
from pathlib import Path
import threading
import uuid


@dataclass
class TokenUsage:
    responses: int = 0
    missing_usage: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    total_tokens: int = 0
    models: set[str] = field(default_factory=set)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def snapshot(self):
        with self.lock:
            return {
                "responses": self.responses, "missing_usage": self.missing_usage,
                "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "cache_read_input_tokens": self.cache_read_input_tokens,
                "cache_creation_input_tokens": self.cache_creation_input_tokens,
                "total_tokens": self.total_tokens, "models": sorted(self.models),
            }


_current: ContextVar[TokenUsage | None] = ContextVar("token_usage", default=None)


def record_usage(model: str, *, input_tokens: int | None = None, output_tokens: int = 0,
                 cache_read_input_tokens: int = 0, cache_creation_input_tokens: int = 0,
                 total_tokens: int = 0):
    usage = _current.get()
    if usage is None:
        return
    with usage.lock:
        usage.responses += 1
        usage.models.add(model)
        if input_tokens is None:
            usage.missing_usage += 1
            return
        usage.input_tokens += input_tokens
        usage.output_tokens += output_tokens
        usage.cache_read_input_tokens += cache_read_input_tokens
        usage.cache_creation_input_tokens += cache_creation_input_tokens
        usage.total_tokens += total_tokens


def track_conversion(function):
    @wraps(function)
    def wrapped(pptx_path, *args, **kwargs):
        usage = TokenUsage()
        token = _current.set(usage)
        conversion_id = uuid.uuid4().hex[:10]
        status = "error"
        try:
            result = function(pptx_path, *args, **kwargs)
            result["token_usage"] = usage.snapshot()
            status = "complete"
            return result
        finally:
            _current.reset(token)
            print("[tokens-summary] " + json.dumps({
                "conversion": conversion_id, "file": Path(pptx_path).name,
                "status": status, **usage.snapshot(), "scope": "reported_responses",
            }), flush=True)
    return wrapped
