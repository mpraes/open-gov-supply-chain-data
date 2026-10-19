class FakeAnalyticsCursor:
    """Cursor falso que grava as queries executadas e devolve os conjuntos de linhas na ordem."""

    def __init__(self, result_sets: list[list[tuple[object, ...]]]) -> None:
        self._result_sets = list(result_sets)
        self.queries: list[str] = []
        self._current: list[tuple[object, ...]] = []

    def execute(self, query: str, params: tuple[object, ...] | None = None) -> None:
        self.queries.append(query)
        if not self._result_sets:
            self._current = []
            return
        self._current = self._result_sets.pop(0)

    def fetchone(self) -> tuple[object, ...] | None:
        if not self._current:
            return None
        return self._current[0]

    def fetchall(self) -> list[tuple[object, ...]]:
        return list(self._current)


class FakeAnalyticsConnection:
    """Conexão falsa que abre esse cursor e marca o fechamento."""

    def __init__(self, result_sets: list[list[tuple[object, ...]]]) -> None:
        self.cursor_obj = FakeAnalyticsCursor(result_sets)
        self.closed = False

    def cursor(self) -> FakeAnalyticsCursor:
        return self.cursor_obj

    def close(self) -> None:
        self.closed = True
