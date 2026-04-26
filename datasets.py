"""
ProtonIQ — Simulated Data Engine
All data is realistic dummy data for demo/pitch purposes.
Replace with live feeds post-contract.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ── CONSTANTS ──────────────────────────────────────────────────────────────────
DEPOTS = ["Marondera (HQ)", "Harare Depot", "Bulawayo Depot"]
DEPOT_SHORT = ["Marondera", "Harare", "Bulawayo"]

SKUS = {
    "Proton Superior White Bread 700g": {"category": "Bread", "price": 1.45, "cost": 0.78},
    "Proton Superior Brown Bread 700g": {"category": "Bread", "price": 1.50, "cost": 0.82},
    "Proton White Bread 400g":          {"category": "Bread", "price": 0.85, "cost": 0.45},
    "Proton Ramba Waraira Cookies 200g":{"category": "Cookies", "price": 1.10, "cost": 0.55},
    "Proton Select Cookies 150g":       {"category": "Cookies", "price": 0.95, "cost": 0.48},
    "Proton Strikers Biscuits 150g":    {"category": "Biscuits", "price": 0.90, "cost": 0.42},
    "Proton Candy Cakes 6pk":           {"category": "Cakes", "price": 1.20, "cost": 0.60},
    "Proton Hot Dog Rolls 6pk":         {"category": "Rolls", "price": 1.35, "cost": 0.68},
    "Proton Burger Rolls 4pk":          {"category": "Rolls", "price": 1.15, "cost": 0.58},
    "Proton Jumbo Buns 4pk":            {"category": "Rolls", "price": 1.00, "cost": 0.50},
    "Proton Hot Cross Buns 6pk":        {"category": "Rolls", "price": 1.30, "cost": 0.65},
    "Proton Instant Sponge Cake Mix":   {"category": "Cake Mix", "price": 2.10, "cost": 1.05},
}

RETAILERS = [
    "TM Pick n Pay Harare",
    "TM Pick n Pay Bulawayo",
    "OK Zimbabwe Marondera",
    "OK Zimbabwe Harare",
    "Spar Harare",
    "Spar Gweru",
    "SaiMart Harare",
    "Choppies Harare",
    "Choppies Bulawayo",
    "Wholesale Distributors",
    "Schools & Institutions",
    "Hospitals & NGOs",
]

CHANNELS = ["Supermarkets", "Wholesale", "Institutions", "Tuck Shops"]

FLEET = [
    {"id": "ZB-001", "type": "10-Tonne Truck", "depot": "Marondera"},
    {"id": "ZB-002", "type": "10-Tonne Truck", "depot": "Marondera"},
    {"id": "ZB-003", "type": "5-Tonne Truck",  "depot": "Marondera"},
    {"id": "ZH-001", "type": "10-Tonne Truck", "depot": "Harare"},
    {"id": "ZH-002", "type": "5-Tonne Truck",  "depot": "Harare"},
    {"id": "ZH-003", "type": "Sprinter Van",   "depot": "Harare"},
    {"id": "ZBw-01", "type": "10-Tonne Truck", "depot": "Bulawayo"},
    {"id": "ZBw-02", "type": "Sprinter Van",   "depot": "Bulawayo"},
]

ROUTES = [
    "Marondera → Harare CBD",
    "Marondera → Harare South",
    "Marondera → Chitungwiza",
    "Harare → Marondera",
    "Harare → Gweru",
    "Harare → Chinhoyi",
    "Bulawayo → Gwanda",
    "Bulawayo → Gweru",
]

# ── DATE RANGE ─────────────────────────────────────────────────────────────────
END_DATE = datetime(2025, 3, 31)
START_DATE = END_DATE - timedelta(days=364)
DATES = pd.date_range(START_DATE, END_DATE, freq="D")
WEEKS = pd.date_range(START_DATE, END_DATE, freq="W-MON")
MONTHS = pd.date_range("2024-04-01", END_DATE, freq="MS")

# ──────────────────────────────────────────────────────────────────────────────
# 1. PRODUCTION OUTPUT
# ──────────────────────────────────────────────────────────────────────────────
def get_production_data():
    rows = []
    for date in DATES:
        is_sun = date.weekday() == 6
        for sku, info in SKUS.items():
            base = {
                "Bread": 18000, "Cookies": 9000, "Biscuits": 7000,
                "Cakes": 5000, "Rolls": 6000, "Cake Mix": 2000
            }[info["category"]]
            if is_sun:
                base = int(base * 0.4)
            noise = np.random.normal(1.0, 0.07)
            trend = 1 + (date - START_DATE).days / 365 * 0.10
            qty = max(0, int(base * noise * trend))
            rows.append({
                "date": date, "sku": sku, "category": info["category"],
                "units_produced": qty, "unit_cost": info["cost"],
                "unit_price": info["price"],
                "cogs": round(qty * info["cost"], 2),
                "revenue_potential": round(qty * info["price"], 2),
            })
    return pd.DataFrame(rows)

# ──────────────────────────────────────────────────────────────────────────────
# 2. DEPOT INTELLIGENCE
# ──────────────────────────────────────────────────────────────────────────────
def get_depot_data():
    rows = []
    depot_dispatch = {"Marondera (HQ)": 0.55, "Harare Depot": 0.30, "Bulawayo Depot": 0.15}
    for date in DATES:
        for depot, share in depot_dispatch.items():
            total_units = int(np.random.normal(85000, 5000) * share)
            dispatched  = int(total_units * np.random.uniform(0.88, 0.98))
            returned    = int((total_units - dispatched) * np.random.uniform(0.05, 0.15))
            rows.append({
                "date": date, "depot": depot,
                "units_received": total_units,
                "units_dispatched": dispatched,
                "units_returned": returned,
                "fill_rate": round(dispatched / total_units * 100, 1),
                "waste_units": returned,
            })
    return pd.DataFrame(rows)

# ──────────────────────────────────────────────────────────────────────────────
# 3. RETAILER PERFORMANCE
# ──────────────────────────────────────────────────────────────────────────────
def get_retailer_data():
    rows = []
    retailer_weights = {
        "TM Pick n Pay Harare": 0.18, "TM Pick n Pay Bulawayo": 0.10,
        "OK Zimbabwe Marondera": 0.06, "OK Zimbabwe Harare": 0.14,
        "Spar Harare": 0.10, "Spar Gweru": 0.05,
        "SaiMart Harare": 0.07, "Choppies Harare": 0.09,
        "Choppies Bulawayo": 0.06, "Wholesale Distributors": 0.08,
        "Schools & Institutions": 0.04, "Hospitals & NGOs": 0.03,
    }
    for month in MONTHS:
        for retailer, weight in retailer_weights.items():
            revenue = round(np.random.normal(120000 * weight, 8000 * weight), 2)
            units   = int(revenue / 1.20)
            on_time = round(np.random.uniform(82, 98), 1)
            rows.append({
                "month": month, "retailer": retailer, "revenue_usd": revenue,
                "units_sold": units, "on_time_delivery_pct": on_time,
                "channel": "Supermarkets" if "Pick" in retailer or "OK" in retailer or "Spar" in retailer or "Choppies" in retailer
                           else ("Wholesale" if "Wholesale" in retailer
                           else ("Institutions" if "Schools" in retailer or "Hospitals" in retailer
                           else "Supermarkets"))
            })
    return pd.DataFrame(rows)

# ──────────────────────────────────────────────────────────────────────────────
# 4. SKU INTELLIGENCE
# ──────────────────────────────────────────────────────────────────────────────
def get_sku_data():
    prod = get_production_data()
    monthly = prod.groupby([pd.Grouper(key="date", freq="MS"), "sku", "category"]).agg(
        units_produced=("units_produced", "sum"),
        revenue_potential=("revenue_potential", "sum"),
        cogs=("cogs", "sum"),
    ).reset_index()
    monthly["gross_margin_pct"] = round((monthly["revenue_potential"] - monthly["cogs"]) / monthly["revenue_potential"] * 100, 1)
    monthly["month"] = monthly["date"]
    return monthly

# ──────────────────────────────────────────────────────────────────────────────
# 5. FLEET PERFORMANCE
# ──────────────────────────────────────────────────────────────────────────────
def get_fleet_data():
    rows = []
    for week in WEEKS:
        for v in FLEET:
            trips   = np.random.randint(3, 9)
            on_time = round(np.random.uniform(80, 97), 1)
            km      = int(np.random.normal(450, 80))
            fuel    = round(km * np.random.uniform(0.28, 0.35), 1)
            rows.append({
                "week": week, "vehicle_id": v["id"],
                "vehicle_type": v["type"], "depot": v["depot"],
                "trips_completed": trips, "on_time_pct": on_time,
                "km_driven": km, "fuel_litres": fuel,
                "fuel_efficiency_km_l": round(km / fuel, 2),
                "maintenance_due": np.random.choice([True, False], p=[0.1, 0.9]),
            })
    return pd.DataFrame(rows)

# ──────────────────────────────────────────────────────────────────────────────
# SUMMARY KPIs (for Executive Command Centre)
# ──────────────────────────────────────────────────────────────────────────────
def get_executive_kpis():
    prod = get_production_data()
    depot = get_depot_data()
    ret = get_retailer_data()

    last30 = prod[prod["date"] >= (END_DATE - timedelta(days=30))]
    prev30 = prod[(prod["date"] >= (END_DATE - timedelta(days=60))) & (prod["date"] < (END_DATE - timedelta(days=30)))]

    total_rev   = last30["revenue_potential"].sum()
    prev_rev    = prev30["revenue_potential"].sum()
    rev_growth  = round((total_rev - prev_rev) / prev_rev * 100, 1)

    total_units = last30["units_produced"].sum()
    fill_rate   = round(depot[depot["date"] >= (END_DATE - timedelta(days=30))]["fill_rate"].mean(), 1)
    waste_pct   = round(depot["waste_units"].sum() / depot["units_received"].sum() * 100, 2)

    return {
        "revenue_30d": round(total_rev),
        "revenue_growth_pct": rev_growth,
        "units_30d": total_units,
        "fill_rate": fill_rate,
        "waste_pct": waste_pct,
        "active_retailers": len(RETAILERS),
        "fleet_vehicles": len(FLEET),
        "depots": len(DEPOTS),
    }
