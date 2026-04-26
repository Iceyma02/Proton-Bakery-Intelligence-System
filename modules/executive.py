"""
ProtonIQ Module 5 — Executive Command Centre
Top-level KPIs, summary visuals, and CEO-level overview.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import (apply_theme, COLOR_SEQUENCE, PROTON_GREEN_MID,
                           PROTON_GOLD, PROTON_RED, PROTON_GREEN_LIGHT,
                           PROTON_DARK_CARD, PROTON_TEXT, PROTON_TEXT_DIM)

def kpi_card(label, value, sub, color=PROTON_GREEN_LIGHT, icon="📊"):
    return html.Div([
        html.Div(icon, className="exec-icon"),
        html.Div(value, className="exec-value", style={"color": color}),
        html.Div(label, className="exec-label"),
        html.Div(sub,   className="exec-sub"),
    ], className="exec-kpi-card")

def render_executive(kpis, prod_df, ret_df, depot_df, fleet_df):
    # ── Top KPI Cards Row
    cards_row = dbc.Row([
        dbc.Col(kpi_card("Revenue (30d)",  f"${kpis['revenue_30d']:,}",
                         f"{'+' if kpis['revenue_growth_pct']>0 else ''}{kpis['revenue_growth_pct']}% vs prev 30d",
                         PROTON_GOLD, "💰"), md=3),
        dbc.Col(kpi_card("Units Produced (30d)", f"{kpis['units_30d']:,}",
                         "Across all SKUs & categories", PROTON_GREEN_LIGHT, "🏭"), md=3),
        dbc.Col(kpi_card("Avg Fill Rate",  f"{kpis['fill_rate']}%",
                         "All depots — 30-day average",
                         PROTON_GREEN_LIGHT if kpis['fill_rate'] >= 90 else PROTON_RED, "🚚"), md=3),
        dbc.Col(kpi_card("Waste Rate",     f"{kpis['waste_pct']}%",
                         "Returns as % of dispatched",
                         PROTON_GREEN_LIGHT if kpis['waste_pct'] < 3 else PROTON_RED, "♻️"), md=3),
    ], className="mb-3")

    second_row = dbc.Row([
        dbc.Col(kpi_card("Retail Partners", str(kpis['active_retailers']),
                         "TM, OK, Spar, Choppies + more", PROTON_GOLD, "🏪"), md=3),
        dbc.Col(kpi_card("Fleet Vehicles",  str(kpis['fleet_vehicles']),
                         "Across 3 depots", PROTON_GREEN_LIGHT, "🚛"), md=3),
        dbc.Col(kpi_card("Active Depots",   str(kpis['depots']),
                         "Marondera · Harare · Bulawayo", PROTON_GREEN_LIGHT, "📍"), md=3),
        dbc.Col(kpi_card("Years Operating", "63+",
                         "Established 1961 — Superbrand 2021", PROTON_GOLD, "🏆"), md=3),
    ], className="mb-3")

    # ── Revenue 12-month overview
    monthly_rev = prod_df.groupby(pd.Grouper(key="date", freq="MS"))["revenue_potential"].sum().reset_index()
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=monthly_rev["date"], y=monthly_rev["revenue_potential"],
        fill="tozeroy", line=dict(color=PROTON_GREEN_MID, width=3),
        fillcolor="rgba(46,139,87,0.15)",
        name="Revenue Potential",
        hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    apply_theme(fig_rev, "Monthly Revenue Potential — 12-Month Overview")

    # ── Retailer Revenue Pie
    ret_agg = ret_df.groupby("retailer")["revenue_usd"].sum().reset_index()
    fig_pie = px.pie(
        ret_agg, names="retailer", values="revenue_usd",
        hole=0.5, color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig_pie.update_traces(
        textposition="outside",
        textfont=dict(color="white", size=9),
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<extra></extra>",
    )
    apply_theme(fig_pie, "Revenue Share by Retail Partner")

    # ── Fleet avg OTD gauge
    avg_otd = fleet_df["on_time_pct"].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_otd,
        delta={"reference": 90, "valueformat": ".1f"},
        title={"text": "Fleet On-Time Delivery", "font": {"color": PROTON_TEXT, "size": 14}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": PROTON_TEXT_DIM},
            "bar": {"color": PROTON_GREEN_MID},
            "bgcolor": PROTON_DARK_CARD,
            "bordercolor": PROTON_GREEN_MID,
            "steps": [
                {"range": [0, 80],  "color": "rgba(192,57,43,0.3)"},
                {"range": [80, 90], "color": "rgba(212,160,23,0.3)"},
                {"range": [90, 100],"color": "rgba(46,139,87,0.3)"},
            ],
            "threshold": {"line": {"color": PROTON_GOLD, "width": 3}, "thickness": 0.8, "value": 90},
        },
        number={"suffix": "%", "font": {"color": PROTON_GOLD, "size": 36}},
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color=PROTON_TEXT),
                            margin=dict(l=30, r=30, t=40, b=20))

    # ── Depot fill rate comparison (latest month)
    depot_latest = depot_df[depot_df["date"] >= depot_df["date"].max() - pd.Timedelta(days=30)]
    depot_fill = depot_latest.groupby("depot")["fill_rate"].mean().reset_index()
    fig_depot = px.bar(
        depot_fill, x="depot", y="fill_rate",
        color="fill_rate",
        color_continuous_scale=["#C0392B", "#2E8B57", "#D4A017"],
        labels={"fill_rate": "Fill Rate (%)", "depot": ""},
        text=depot_fill["fill_rate"].apply(lambda x: f"{x:.1f}%"),
    )
    fig_depot.update_traces(textposition="outside", textfont=dict(color="white"))
    fig_depot.update_coloraxes(showscale=False)
    fig_depot.add_hline(y=90, line_dash="dot", line_color=PROTON_GOLD)
    apply_theme(fig_depot, "Depot Fill Rate — Current Month")

    return html.Div([
        cards_row,
        second_row,
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_rev,   config={"displayModeBar": False}), md=8, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_gauge, config={"displayModeBar": False}), md=4, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pie,   config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_depot, config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
    ])
