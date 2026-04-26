"""
ProtonIQ Module 4 — SKU Intelligence
Product-level performance, margin analysis, and volume trends.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import apply_theme, COLOR_SEQUENCE, PROTON_GREEN_MID, PROTON_GOLD

def render_sku(sku_df):
    # ── Top SKUs by Revenue Potential (bubble)
    sku_agg = sku_df.groupby("sku").agg(
        revenue=("revenue_potential", "sum"),
        units=("units_produced", "sum"),
        margin=("gross_margin_pct", "mean"),
        cogs=("cogs", "sum"),
    ).reset_index()
    sku_agg["short_name"] = sku_agg["sku"].apply(lambda x: x.replace("Proton ", "").replace(" 700g", "").replace(" 200g", "").replace(" 150g", "").replace(" 6pk", "").replace(" 4pk", ""))

    fig_bubble = px.scatter(
        sku_agg, x="units", y="revenue", size="margin",
        color="margin", text="short_name",
        color_continuous_scale=["#122B1E", "#2E8B57", "#D4A017"],
        labels={"units": "Units Produced", "revenue": "Revenue Potential (USD)", "margin": "Gross Margin %"},
    )
    fig_bubble.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
    apply_theme(fig_bubble, "SKU Performance Matrix — Volume vs Revenue vs Margin")

    # ── Margin Bar by SKU
    sku_margin = sku_agg.sort_values("margin", ascending=True)
    fig_margin = px.bar(
        sku_margin, x="margin", y="short_name", orientation="h",
        color="margin",
        color_continuous_scale=["#C0392B", "#2E8B57", "#D4A017"],
        labels={"margin": "Gross Margin (%)", "short_name": ""},
    )
    fig_margin.update_coloraxes(showscale=False)
    apply_theme(fig_margin, "Gross Margin % by SKU")

    # ── Monthly volume trend for top 5 SKUs
    top5 = sku_agg.nlargest(5, "revenue")["sku"].tolist()
    top5_monthly = sku_df[sku_df["sku"].isin(top5)].copy()
    top5_monthly["short"] = top5_monthly["sku"].apply(lambda x: x.replace("Proton ", ""))

    fig_trend = px.line(
        top5_monthly, x="month", y="units_produced", color="short",
        color_discrete_sequence=COLOR_SEQUENCE,
        markers=True,
        labels={"units_produced": "Units Produced", "month": "", "short": "SKU"},
    )
    apply_theme(fig_trend, "Top 5 SKU Production Trends — Monthly")

    # ── Revenue vs COGS waterfall concept (bar comparison)
    fig_waterfall = go.Figure()
    sku_agg_sorted = sku_agg.sort_values("revenue", ascending=False).head(8)
    fig_waterfall.add_trace(go.Bar(
        name="Revenue Potential", x=sku_agg_sorted["short_name"],
        y=sku_agg_sorted["revenue"],
        marker_color=PROTON_GREEN_MID, opacity=0.9,
    ))
    fig_waterfall.add_trace(go.Bar(
        name="COGS", x=sku_agg_sorted["short_name"],
        y=sku_agg_sorted["cogs"],
        marker_color=PROTON_GOLD, opacity=0.7,
    ))
    fig_waterfall.update_layout(barmode="overlay")
    apply_theme(fig_waterfall, "Revenue vs Cost of Goods — Top 8 SKUs")

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_bubble, config={"displayModeBar": False}), md=8, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_margin, config={"displayModeBar": False}), md=4, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_trend,     config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_waterfall, config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
    ])
