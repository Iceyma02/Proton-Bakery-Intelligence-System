"""
ProtonIQ Module 6 — Fleet Performance
Vehicle tracking, route efficiency, fuel consumption, and maintenance alerts.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from assets.theme import apply_theme, COLOR_SEQUENCE, PROTON_RED, PROTON_GOLD, PROTON_GREEN_MID

def render_fleet(fleet_df):
    # ── Per-vehicle aggregates
    veh_otd = fleet_df.groupby("vehicle_id").agg(
        avg_otd=("on_time_pct", "mean"),
        total_km=("km_driven", "sum"),
        total_fuel=("fuel_litres", "sum"),
        trips=("trips_completed", "sum"),
        depot=("depot", "first"),
        vtype=("vehicle_type", "first"),
    ).reset_index().sort_values("avg_otd", ascending=True)

    # OTD horizontal bar
    fig_otd = px.bar(
        veh_otd, x="avg_otd", y="vehicle_id", orientation="h",
        color="avg_otd",
        color_continuous_scale=["#C0392B", "#2E8B57", "#D4A017"],
        labels={"avg_otd": "On-Time Delivery (%)", "vehicle_id": "Vehicle"},
        text=veh_otd["avg_otd"].apply(lambda x: f"{x:.1f}%"),
    )
    fig_otd.update_traces(textposition="outside", textfont=dict(color="white"))
    fig_otd.update_coloraxes(showscale=False)
    fig_otd.add_vline(x=90, line_dash="dot", line_color=PROTON_GOLD,
                      annotation_text="Target 90%", annotation_font_color=PROTON_GOLD)
    apply_theme(fig_otd, "On-Time Delivery by Vehicle — All Time")

    # Fuel scatter
    fig_fuel = px.scatter(
        veh_otd, x="total_km", y="total_fuel",
        color="depot", size="trips", text="vehicle_id",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"total_km": "Total KM Driven", "total_fuel": "Total Fuel Used (L)", "depot": "Depot"},
    )
    fig_fuel.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
    apply_theme(fig_fuel, "Fuel Consumption vs Distance by Vehicle")

    # Weekly KM by depot — week column is already datetime, no Grouper needed
    weekly_km = fleet_df.groupby(["week", "depot"])["km_driven"].sum().reset_index()
    fig_km = px.line(
        weekly_km, x="week", y="km_driven", color="depot",
        color_discrete_sequence=COLOR_SEQUENCE, markers=True,
        labels={"km_driven": "KM Driven", "week": "", "depot": "Depot"},
    )
    apply_theme(fig_km, "Weekly KM Driven by Depot")

    # Maintenance alerts — always a Graph, never a bare Div
    maint_due = fleet_df[fleet_df["maintenance_due"]].groupby("vehicle_id").size().reset_index(name="alerts")
    if not maint_due.empty:
        fig_maint = px.bar(
            maint_due, x="vehicle_id", y="alerts",
            color_discrete_sequence=[PROTON_RED],
            labels={"alerts": "Alert Count", "vehicle_id": "Vehicle"},
        )
        apply_theme(fig_maint, "Maintenance Alerts")
    else:
        fig_maint = go.Figure()
        fig_maint.add_annotation(
            text="No maintenance alerts", showarrow=False,
            font=dict(color=PROTON_GREEN_MID, size=14),
            xref="paper", yref="paper", x=0.5, y=0.5,
        )
        apply_theme(fig_maint, "Maintenance Alerts")

    # Summary table
    tbl = veh_otd[["vehicle_id", "vtype", "depot", "trips", "total_km", "avg_otd"]].copy()
    tbl["total_km"] = tbl["total_km"].apply(lambda x: f"{x:,}")
    tbl["avg_otd"]  = tbl["avg_otd"].apply(lambda x: f"{x:.1f}%")
    tbl.columns     = ["Vehicle", "Type", "Depot", "Trips", "Total KM", "OTD %"]
    rows = [html.Tr([html.Th(c) for c in tbl.columns], className="fleet-header")]
    for _, row in tbl.iterrows():
        rows.append(html.Tr([html.Td(v) for v in row], className="fleet-row"))

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_otd,  config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_fuel, config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_km,   config={"displayModeBar": False}), md=8, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_maint,config={"displayModeBar": False}), md=4, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Fleet Roster Summary", className="module-subtitle"),
                html.Div(html.Table(rows, className="fleet-table"), className="fleet-table-wrap"),
            ], md=12, className="mb-3"),
        ]),
    ])
