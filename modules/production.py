"""
ProtonIQ Module 1 — Production Output Tracker
Daily & weekly production intelligence across all SKUs.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import apply_theme, PROTON_GREEN_MID, PROTON_GOLD, PROTON_GREEN_LIGHT, COLOR_SEQUENCE

def render_production(prod_df):
    # ── Daily Production by Category (line)
    daily_cat = prod_df.groupby(["date", "category"])["units_produced"].sum().reset_index()
    fig_trend = px.line(
        daily_cat, x="date", y="units_produced", color="category",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"units_produced": "Units Produced", "date": "", "category": "Category"},
    )
    fig_trend.update_traces(line=dict(width=2))
    apply_theme(fig_trend, "Daily Production Volume — All Categories")

    # ── Monthly Revenue Potential (bar)
    monthly = prod_df.groupby([pd.Grouper(key="date", freq="MS"), "category"]).agg(
        revenue=("revenue_potential", "sum"),
        units=("units_produced", "sum"),
    ).reset_index()
    fig_bar = px.bar(
        monthly, x="date", y="revenue", color="category",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"revenue": "Revenue Potential (USD)", "date": "", "category": "Category"},
        barmode="stack",
    )
    apply_theme(fig_bar, "Monthly Revenue Potential by Category")

    # ── SKU Volume Treemap (last 30 days)
    last30 = prod_df[prod_df["date"] >= prod_df["date"].max() - pd.Timedelta(days=30)]
    sku_vol = last30.groupby(["category", "sku"])["units_produced"].sum().reset_index()
    fig_tree = px.treemap(
        sku_vol, path=["category", "sku"], values="units_produced",
        color="units_produced",
        color_continuous_scale=["#122B1E", "#2E8B57", "#D4A017"],
    )
    fig_tree.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=30, b=0))
    fig_tree.update_traces(
        textfont=dict(color="white", size=12),
        hovertemplate="<b>%{label}</b><br>Units: %{value:,.0f}<extra></extra>",
    )

    # ── Gross Margin by Category (donut)
    margin_df = prod_df.groupby("category").agg(
        rev=("revenue_potential", "sum"),
        cost=("cogs", "sum"),
    ).reset_index()
    margin_df["margin"] = margin_df["rev"] - margin_df["cost"]
    fig_donut = px.pie(
        margin_df, names="category", values="margin",
        hole=0.6, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig_donut.update_traces(
        textposition="outside",
        textfont=dict(color="white"),
        hovertemplate="<b>%{label}</b><br>Gross Margin: $%{value:,.0f}<extra></extra>",
    )
    apply_theme(fig_donut, "Gross Margin Contribution by Category")

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_trend, config={"displayModeBar": False}), md=12, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_bar,  config={"displayModeBar": False}), md=8, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_donut,config={"displayModeBar": False}), md=4, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.P("SKU Volume Breakdown — Last 30 Days", className="module-subtitle"),
                dcc.Graph(figure=fig_tree, config={"displayModeBar": False}, style={"height": "320px"}),
            ], md=12),
        ]),
    ])
