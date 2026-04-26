"""
ProtonIQ Brand Theme
Exact colours extracted from Proton Bakers logo PNG.
Primary green: #00782D | Cream text: #E1E1A5 | Dark bg: deep forest
"""

# ── EXACT PROTON BRAND PALETTE (from logo pixel analysis) ─────────────────────
PROTON_GREEN       = "#00692D"   # exact logo dark green
PROTON_GREEN_MID   = "#00782D"   # exact logo primary green
PROTON_GREEN_LIGHT = "#00964B"   # lighter logo green (highlight areas)
PROTON_CREAM       = "#E1E1A5"   # exact logo cream/text colour
PROTON_CREAM_WARM  = "#F0E1B4"   # warm cream variant from logo
PROTON_GOLD        = "#C8B86E"   # muted gold derived from cream tones
PROTON_GOLD_LIGHT  = "#E1E1A5"   # bright cream-gold (logo text colour)
PROTON_DARK        = "#001A0D"   # near-black deep forest
PROTON_DARK_MID    = "#002B14"   # dark card bg
PROTON_DARK_CARD   = "#003319"   # card surfaces
PROTON_BORDER      = "#005522"   # subtle borders
PROTON_TEXT        = "#E8F5E9"   # off-white text
PROTON_TEXT_DIM    = "#6DBF82"   # muted green text
PROTON_RED         = "#C0392B"   # alert red
PROTON_ORANGE      = "#E67E22"   # warning orange

COLOR_SEQUENCE = [
    "#00782D",   # proton primary green
    "#E1E1A5",   # proton cream
    "#00964B",   # bright green
    "#C8B86E",   # warm gold
    "#33A85A",   # mid green
    "#F0E1B4",   # warm cream
    "#4DB6AC",   # teal accent
    "#FF8A65",   # warm orange
    "#BA68C8",   # purple
    "#64B5F6",   # blue
    "#81C784",   # light green
    "#FFB74D",   # amber
]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'DM Sans', sans-serif", color=PROTON_TEXT, size=12),
    title_font=dict(family="'DM Sans', sans-serif", color=PROTON_TEXT, size=14),
    legend=dict(
        bgcolor="rgba(0,51,25,0.8)",
        bordercolor=PROTON_BORDER,
        borderwidth=1,
        font=dict(color=PROTON_TEXT, size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(0,120,45,0.12)",
        zerolinecolor="rgba(0,120,45,0.2)",
        tickfont=dict(color=PROTON_TEXT_DIM, size=11),
        linecolor=PROTON_BORDER,
    ),
    yaxis=dict(
        gridcolor="rgba(0,120,45,0.12)",
        zerolinecolor="rgba(0,120,45,0.2)",
        tickfont=dict(color=PROTON_TEXT_DIM, size=11),
        linecolor=PROTON_BORDER,
    ),
    margin=dict(l=40, r=20, t=40, b=40),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor=PROTON_DARK_MID,
        bordercolor=PROTON_GREEN_MID,
        font=dict(color=PROTON_TEXT, size=12),
    ),
    colorway=COLOR_SEQUENCE,
)

def apply_theme(fig, title=None):
    fig.update_layout(**CHART_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, x=0.02, xanchor="left"))
    return fig
