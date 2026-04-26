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
    # ── Weekly OTD by Vehicle
    veh_otd = fleet_df.groupby("vehicle_id").agg(
        avg_otd=("on_time_pct", "mean"),
        total_km=("km_driven", "sum"),
        total_fuel=("fuel_litres", "sum"),
        trips=("trips_completed", "sum"),
        depot=("depot", "first"),
        vtype=("vehicle_type", "first"),
    ).reset_index().sort_values("avg_otd", ascending=True)

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

    # ── Fuel Efficiency Scatter
    fig_fuel = px.scatter(
        veh_otd, x="total_km", y="fuel_litres",
        color="depot", size="trips",
        text="vehicle_id",
        color_discrete_sequence=COLOR_SEQUENCE,
        labels={"total_km": "Total KM Driven", "fuel_litres": "Total Fuel Used (L)", "depot": "Depot"},
    )
    fig_fuel.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
    apply_theme(fig_fuel, "Fuel Consumption vs Distance by Vehicle")

    # ── Weekly KM Trend per Depot
    weekly_km = fleet_df.groupby([pd.Grouper(key="week", freq="W"), "depot"])["km_driven"].sum().reset_index()
    fig_km = px.line(
        weekly_km, x="week", y="km_driven", color="depot",
        color_discrete_sequence=COLOR_SEQUENCE,
        markers=True,
        labels={"km_driven": "KM Driven", "week": "", "depot": "Depot"},
    )
    apply_theme(fig_km, "Weekly KM Driven by Depot")

    # ── Maintenance Due Alerts
    maintenance_due = fleet_df[fleet_df["maintenance_due"]].groupby("vehicle_id").size().reset_index(name="alerts")
    if not maintenance_due.empty:
        fig_maint = px.bar(
            maintenance_due, x="vehicle_id", y="alerts",
            color_discrete_sequence=[PROTON_RED],
            labels={"alerts": "Maintenance Alert Count", "vehicle_id": "Vehicle"},
        )
        apply_theme(fig_maint, "⚠️ Maintenance Alerts by Vehicle")
        maint_chart = dcc.Graph(figure=fig_maint, config={"displayModeBar": False})
    else:
        maint_chart = html.Div("✅ No maintenance alerts detected", className="alert-none")

    # ── Fleet summary table
    table_data = veh_otd[["vehicle_id", "vtype", "depot", "trips", "total_km", "avg_otd"]].copy()
    table_data["total_km"] = table_data["total_km"].apply(lambda x: f"{x:,}")
    table_data["avg_otd"]  = table_data["avg_otd"].apply(lambda x: f"{x:.1f}%")
    table_data.columns     = ["Vehicle", "Type", "Depot", "Trips", "Total KM", "OTD %"]

    rows = [html.Tr([html.Th(c) for c in table_data.columns], className="fleet-header")]
    for _, row in table_data.iterrows():
        rows.append(html.Tr([html.Td(v) for v in row], className="fleet-row"))
    fleet_table = html.Table(rows, className="fleet-table")

    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_otd, config={"displayModeBar": False}), md=6, className="mb-3"),
            dbc.Col(dcc.Graph(figure=fig_fuel,config={"displayModeBar": False}), md=6, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_km,  config={"displayModeBar": False}), md=8, className="mb-3"),
            dbc.Col(maint_chart, md=4, className="mb-3"),
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Fleet Roster Summary", className="module-subtitle"),
                html.Div(fleet_table, className="fleet-table-wrap"),
            ], md=12, className="mb-3"),
        ]),
    ])
