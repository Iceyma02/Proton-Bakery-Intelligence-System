"""
ProtonIQ Module 3 — Retailer Performance
Revenue, on-time delivery, and channel breakdown across 12 retail partners.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import apply_theme, COLOR_SEQUENCE, PROTON_GOLD, PROTON_RED, PROTON_GREEN_LIGHT

def render_retailer(ret_df):
    # ── Revenue by Retailer (horizontal bar, latest 6 months)
    rev_agg = ret_df.groupby("retailer")["revenue_usd"].sum().reset_index().sort_values("revenue_usd", ascending=True)
    fig_hbar = px.bar(
        rev_agg, x="revenue_usd", y="retailer", orientation="h",
        color="revenue_usd",
        color_continuous_scale=["#122B1E", "#2E8B57", "#D4A017"],
        labels={"revenue_usd": "Total Revenue (USD)", "retailer": ""},
    )
    fig_hbar.update_coloraxes(showscale=False)
    apply_theme(fig_hbar, "Retailer Revenue Ranking — All Time")

    # ── Revenue Trend by Channel
    channel_monthly = ret_df.groupby([pd.Grouper(key="month", freq="MS"), "channel"])["revenue_usd"].sum().reset_index()
    fig_channel = px.area(
        channel_monthly, x="month", y="revenue_usd", color="channel",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"revenue_usd": "Revenue (USD)", "month": "", "channel": "Channel"},
    )
    fig_channel.update_traces(opacity=0.7)
    apply_theme(fig_channel, "Revenue by Channel — Monthly Trend")

    # ── On-Time Delivery Scatter
    otd = ret_df.groupby("retailer").agg(
        revenue=("revenue_usd", "sum"),
        otd=("on_time_delivery_pct", "mean"),
    ).reset_index()
    fig_scatter = px.scatter(
        otd, x="otd", y="revenue", text="retailer",
        size="revenue", color="revenue",
        color_continuous_scale=["#122B1E", "#2E8B57", "#D4A017"],
        labels={"otd": "On-Time Delivery (%)", "revenue": "Total Revenue (USD)", "retailer": "Retailer"},
    )
    fig_scatter.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
    fig_scatter.update_coloraxes(showscale=False)
    fig_scatter.add_vline(x=90, line_dash="dot", line_color=PROTON_GOLD,
                          annotation_text="Target OTD 90%", annotation_font_color=PROTON_GOLD)
    apply_theme(fig_scatter, "Revenue vs On-Time Delivery by Retailer")

    # ── Monthly revenue heatmap (retailer × month)
    pivot = ret_df.pivot_table(index="retailer", columns=ret_df["month"].dt.strftime("%b %Y"), values="revenue_usd", aggfunc="sum")
    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[[0, "#0D2818"], [0.5, "#2E8B57"], [1, "#D4A017"]],
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>%{x}<br>Revenue: $%{z:,.0f}<extra></extra>",
    ))
    apply_theme(fig_heat, "Retailer Revenue Heatmap — Month × Partner")

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_hbar,    config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_scatter, config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_channel, config={"displayModeBar": False}), md=12, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_heat,    config={"displayModeBar": False}), md=12, className="mb-3"),
        ]),
    ])
