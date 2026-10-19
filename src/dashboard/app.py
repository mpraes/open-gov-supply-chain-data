"""Aplicação FastAPI do dashboard de KPIs de compras públicas."""

import os
from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dashboard.db import AnalyticsConnection, connect_analytics
from dashboard.kpis.load_theme import THEMES, load_theme_kpis, theme_kpis_json
from dashboard.kpis.timeframe import parse_timeframe
from dashboard.settings import load_dashboard_settings
from observability.logging_json import get_json_logger, log_error

_APP_DIR = Path(__file__).parent
_TEMPLATES = Jinja2Templates(directory=str(_APP_DIR / "templates"))
_LOG = get_json_logger("dashboard")
ConnectFactory = Callable[[], AnalyticsConnection]

_PAGE_TITLES = {
    "overview": "Relatórios",
    "fornecedor": "Fornecedor",
    "material": "Material",
    "servico": "Serviço",
    "uasg": "UASG",
}


def default_connect_factory() -> AnalyticsConnection:
    """Abre o analytics usando DASHBOARD_ENV_FILE ou `.env`.

    Exemplo:
        conn = default_connect_factory()
    """
    raw = os.environ.get("DASHBOARD_ENV_FILE", ".env")
    return connect_analytics(load_dashboard_settings(Path(raw)))


def create_app(*, connect_factory: ConnectFactory) -> FastAPI:
    """Monta a aplicação do dashboard sem abrir o Postgres até uma requisição.

    Exemplo:
        app = create_app(connect_factory=default_connect_factory)
    """
    app = FastAPI(title="Open Gov Analytics")
    app.state.connect_factory = connect_factory
    _mount_static(app)
    _register_pages(app)
    _register_kpis(app, connect_factory)
    return app


def _mount_static(app: FastAPI) -> None:
    """Monta /static a partir do diretório static, criando-o se não existir."""
    static_dir = _APP_DIR / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _register_pages(app: FastAPI) -> None:
    """Registra as rotas HTML de overview, fornecedor, material, servico e uasg."""

    @app.get("/")
    def overview_page(request: Request) -> object:
        """Renderiza a página do tema overview."""
        return _render_page(request, "overview")

    @app.get("/fornecedor")
    def fornecedor_page(request: Request) -> object:
        """Renderiza a página do tema fornecedor."""
        return _render_page(request, "fornecedor")

    @app.get("/material")
    def material_page(request: Request) -> object:
        """Renderiza a página do tema material."""
        return _render_page(request, "material")

    @app.get("/servico")
    def servico_page(request: Request) -> object:
        """Renderiza a página do tema servico."""
        return _render_page(request, "servico")

    @app.get("/uasg")
    def uasg_page(request: Request) -> object:
        """Renderiza a página do tema uasg."""
        return _render_page(request, "uasg")


def _render_page(request: Request, theme: str) -> object:
    """Renderiza page.html com o título e a URL de KPIs do tema."""
    return _TEMPLATES.TemplateResponse(
        request,
        "page.html",
        {
            "theme": theme,
            "title": _PAGE_TITLES[theme],
            "kpi_url": f"/api/kpis/{theme}",
        },
    )


def _register_kpis(app: FastAPI, connect_factory: ConnectFactory) -> None:
    """Registra GET /api/kpis/{theme} com o query param timeframe."""

    @app.get("/api/kpis/{theme}")
    def kpis(theme: str, timeframe: str = "all") -> object:
        """Rejeita theme ou timeframe inválidos com HTTP 400 e devolve o JSON dos KPIs."""
        if theme not in THEMES:
            raise HTTPException(
                status_code=400,
                detail=f"theme expected one of {set(THEMES)}, got {theme!r}",
            )
        try:
            parsed = parse_timeframe(timeframe)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return _load_or_503(connect_factory, theme, parsed)


def _load_or_503(
    connect_factory: ConnectFactory, theme: str, timeframe: str
) -> object:
    """Abre a conexão, carrega os KPIs do tema e responde 503 quando o analytics falha."""
    try:
        conn = connect_factory()
        try:
            payload = load_theme_kpis(theme, conn, timeframe)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as exc:
        log_error(_LOG, "analytics_unavailable", theme=theme, detail=str(exc))
        return JSONResponse(
            {"error": "analytics_unavailable", "detail": "analytics_unavailable"},
            status_code=503,
        )
    return JSONResponse(theme_kpis_json(payload))


app = create_app(connect_factory=default_connect_factory)
