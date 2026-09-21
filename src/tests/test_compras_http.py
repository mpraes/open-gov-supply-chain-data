from clients.compras_http import http_error_body


class FakeHttpBody:
    def __init__(self, text: object) -> None:
        self.text = text
        self.status_code = 200
        self.headers: dict[str, str] = {}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return {}


def test_http_error_body_returns_empty_when_text_is_not_str() -> None:
    assert http_error_body(FakeHttpBody(None)) == ""


def test_http_error_body_truncates_long_text() -> None:
    body = http_error_body(FakeHttpBody("x" * 600))
    assert body == "x" * 500
