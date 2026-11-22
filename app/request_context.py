import re
from contextvars import ContextVar

REQUEST_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def valid_request_id(value: str | None) -> bool:
    return value is not None and REQUEST_ID_PATTERN.fullmatch(value) is not None


def current_request_id() -> str | None:
    return request_id_context.get()
