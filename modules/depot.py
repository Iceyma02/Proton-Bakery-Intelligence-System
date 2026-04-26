"""
ProtonIQ Module 2 — Depot Intelligence
Dispatch, fill rates, waste and inter-depot comparison.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import apply_theme, COLOR_SEQUENCE, PROTON_RED, PROTON_GOLD, PROTON_GREEN_MID

def render_depot(depot_df):
    # ── Fill Rate Over Time per Depot
    monthly = depot_df.groupby([pd.Grouper(key="date", freq="MS"), "depot"]).agg(
        fill_rate=("fill_rate", "mean"),
        dispatched=("units_dispatched", "sum"),
        returned=("units_returned", "sum"),
        received=("units_received", "sum"),
    ).reset_index()

    fig_fill = px.line(
        monthly, x="date", y="fill_rate", color="depot",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"fill_rate": "Fill Rate (%)", "date": "", "depot": "Depot"},
        markers=True,
    )
    fig_fill.add_hline(y=90, line_dash="dot", line_color=PROTON_GOLD,
                       annotation_text="Target 90%", annotation_font_color=PROTON_GOLD)
    apply_theme(fig_fill, "Depot Fill Rate — Monthly Average")

    # ── Units Dispatched vs Received (grouped bar)
    fig_compare = go.Figure()
    for i, depot in enumerate(depot_df["depot"].unique()):
        sub = monthly[monthly["depot"] == depot]
        fig_compare.add_trace(go.Bar(
            name=f"{depot} — Received", x=sub["date"], y=sub["received"],
            marker_color=COLOR_SEQUENCE[i * 2 % len(COLOR_SEQUENCE)], opacity=0.7,
        ))
        fig_compare.add_trace(go.Bar(
            name=f"{depot} — Dispatched", x=sub["date"], y=sub["dispatched"],
            marker_color=COLOR_SEQUENCE[(i * 2 + 1) % len(COLOR_SEQUENCE)],
        ))
    fig_compare.update_layout(barmode="group")
    apply_theme(fig_compare, "Depot Throughput — Received vs Dispatched")

    # ── Waste / Returns Heatmap Substitute (stacked bar)
    waste_monthly = depot_df.groupby([pd.Grouper(key="date", freq="MS"), "depot"]).agg(
        waste=("units_returned", "sum"),
        total=("units_received", "sum"),
    ).reset_index()
    waste_monthly["waste_pct"] = round(waste_monthly["waste"] / waste_monthly["total"] * 100, 2)

    fig_waste = px.bar(
        waste_monthly, x="date", y="waste_pct", color="depot",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"waste_pct": "Waste / Returns (%)", "date": "", "depot": "Depot"},
        barmode="group",
    )
    fig_waste.add_hline(y=3.0, line_dash="dot", line_color=PROTON_RED,
                        annotation_text="Max 3%", annotation_font_color=PROTON_RED)
    apply_theme(fig_waste, "Depot Waste & Returns Rate")

    # ── Depot summary KPI cards
    latest = depot_df[depot_df["date"] >= depot_df["date"].max() - pd.Timedelta(days=30)]
    kpi_cards = []
    for depot in depot_df["depot"].unique():
        sub = latest[latest["depot"] == depot]
        kpi_cards.append(dbc.Col([
            html.Div([
                html.Div(depot, className="kpi-label"),
                html.Div(f"{sub['fill_rate'].mean():.1f}%", className="kpi-value"),
                html.Div("Avg Fill Rate (30d)", className="kpi-sublabel"),
                html.Hr(className="kpi-divider"),
                html.Div(f"{sub['units_dispatched'].sum():,}", className="kpi-value-sm"),
                html.Div("Units Dispatched", className="kpi-sublabel"),
            ], className="kpi-card"),
        ], md=4))

    return html.Div([
        dbc.Row(kpi_cards, className="mb-3"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_fill,    config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_waste,   config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_compare, config={"displayModeBar": False}), md=12, className="mb-3"),
        ]),
    ])
