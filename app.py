"""
╔══════════════════════════════════════════════════════════════════════╗
║   ProtonIQ — Business Intelligence System                           ║
║   Built by MA TechHub for Proton Bakers (Pvt) Ltd                  ║
║   Established 1961 · The Best of The Best                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

# ── Data & Modules ─────────────────────────────────────────────────────────────
from data.datasets import (
    get_production_data, get_depot_data, get_retailer_data,
    get_sku_data, get_fleet_data, get_executive_kpis,
    DEPOTS, SKUS, RETAILERS,
)
from modules.executive   import render_executive
from modules.production  import render_production
from modules.depot       import render_depot
from modules.retailer    import render_retailer
from modules.sku         import render_sku
from modules.fleet       import render_fleet
from assets.theme        import (
    PROTON_GREEN, PROTON_GREEN_MID, PROTON_GOLD, PROTON_GOLD_LIGHT,
    PROTON_DARK, PROTON_DARK_MID, PROTON_DARK_CARD, PROTON_BORDER,
    PROTON_TEXT, PROTON_TEXT_DIM, PROTON_CREAM,
)

# ── Pre-load all data on startup ───────────────────────────────────────────────
print("⏳ Loading ProtonIQ datasets...")
PROD_DF  = get_production_data()
DEPOT_DF = get_depot_data()
RET_DF   = get_retailer_data()
SKU_DF   = get_sku_data()
FLEET_DF = get_fleet_data()
KPIS     = get_executive_kpis()
print("✅ All datasets loaded.")

# ── App Init ──────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap",
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="ProtonIQ — Business Intelligence",
)
server = app.server

# ── Navigation Items ──────────────────────────────────────────────────────────
NAV_ITEMS = [
    {"id": "executive",  "icon": "🏆", "label": "Command Centre",   "tag": "CEO"},
    {"id": "production", "icon": "🏭", "label": "Production",        "tag": "OPS"},
    {"id": "depot",      "icon": "📦", "label": "Depot Intel",        "tag": "OPS"},
    {"id": "retailer",   "icon": "🏪", "label": "Retailer",           "tag": "SALES"},
    {"id": "sku",        "icon": "📋", "label": "SKU Intel",           "tag": "PROD"},
    {"id": "fleet",      "icon": "🚛", "label": "Fleet",              "tag": "OPS"},
]

MODULE_TITLES = {
    "executive":  ("Executive Command Centre", "CEO-level overview — revenue, fill rates, fleet, retailer performance"),
    "production": ("Production Output Tracker", "Daily & monthly production across all SKUs and categories"),
    "depot":      ("Depot Intelligence",        "Dispatch throughput, fill rates, and waste across all 3 depots"),
    "retailer":   ("Retailer Performance",      "Revenue, on-time delivery, and channel breakdown across 12 partners"),
    "sku":        ("SKU Intelligence",          "Product-level performance, margin analysis, and volume trends"),
    "fleet":      ("Fleet Performance",         "Vehicle OTD, fuel efficiency, route KMs, and maintenance alerts"),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
def build_sidebar():
    nav_links = []
    for item in NAV_ITEMS:
        nav_links.append(
            html.Div(
                id=f"nav-{item['id']}",
                children=[
                    html.Span(item["icon"], className="nav-icon"),
                    html.Span(item["label"], className="nav-label"),
                    html.Span(item["tag"], className=f"nav-tag tag-{item['tag'].lower()}"),
                ],
                className="nav-item",
                n_clicks=0,
            )
        )

    return html.Div([
        # Logo area
        html.Div([
            html.Div([
                html.Div("P", className="logo-letter"),
            ], className="logo-mark"),
            html.Div([
                html.Div("ProtonIQ", className="logo-text"),
                html.Div("Business Intelligence", className="logo-sub"),
            ]),
        ], className="sidebar-logo"),

        html.Div("INTELLIGENCE MODULES", className="nav-section-label"),
        html.Div(nav_links, className="nav-links"),

        # Bottom badge
        html.Div([
            html.Div("🌐 LIVE DEMO", className="live-badge"),
            html.Div("Powered by MA TechHub", className="powered-by"),
            html.Div("protonbakers.com · Since 1961", className="powered-by"),
        ], className="sidebar-footer"),
    ], className="sidebar")

# ── Header ────────────────────────────────────────────────────────────────────
def build_header(active_id):
    title, subtitle = MODULE_TITLES.get(active_id, ("ProtonIQ", ""))
    return html.Div([
        html.Div([
            html.Div([
                html.H1(title, className="page-title"),
                html.P(subtitle, className="page-subtitle"),
            ]),
            html.Div([
                html.Div([
                    html.Span("●", className="live-dot"),
                    html.Span("LIVE DATA", className="live-label"),
                ], className="live-indicator"),
                html.Div("Proton Bakers (Pvt) Ltd", className="company-badge"),
                html.Div("Q1 2025 · Fiscal Year", className="date-badge"),
            ], className="header-right"),
        ], className="header-inner"),
    ], className="page-header")

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div([
    dcc.Store(id="active-module", data="executive"),
    build_sidebar(),
    html.Div([
        html.Div(id="page-header-container"),
        html.Div(id="module-content", className="module-content"),
    ], className="main-area"),
], className="app-root")

# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("active-module", "data"),
    [Input(f"nav-{item['id']}", "n_clicks") for item in NAV_ITEMS],
    [State("active-module", "data")],
    prevent_initial_call=True,
)
def update_active_module(*args):
    states = args[-1]
    ctx = dash.callback_context
    if not ctx.triggered:
        return states
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    module_id = triggered_id.replace("nav-", "")
    return module_id


@app.callback(
    [Output("module-content", "children"),
     Output("page-header-container", "children"),
     *[Output(f"nav-{item['id']}", "className") for item in NAV_ITEMS]],
    Input("active-module", "data"),
)
def render_module(active_id):
    if active_id == "executive":
        content = render_executive(KPIS, PROD_DF, RET_DF, DEPOT_DF, FLEET_DF)
    elif active_id == "production":
        content = render_production(PROD_DF)
    elif active_id == "depot":
        content = render_depot(DEPOT_DF)
    elif active_id == "retailer":
        content = render_retailer(RET_DF)
    elif active_id == "sku":
        content = render_sku(SKU_DF)
    elif active_id == "fleet":
        content = render_fleet(FLEET_DF)
    else:
        content = html.Div("Module not found", style={"color": "white"})

    header = build_header(active_id)
    classes = ["nav-item active" if item["id"] == active_id else "nav-item" for item in NAV_ITEMS]
    return [content, header] + classes


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
