"""
ProtonIQ Brand Theme — Original balanced palette
Forest Green + Wheat Gold. Dark but not overwhelming.
"""

PROTON_GREEN       = "#1A6B35"
PROTON_GREEN_MID   = "#2E8B57"
PROTON_GREEN_LIGHT = "#52B788"
PROTON_GOLD        = "#D4A017"
PROTON_GOLD_LIGHT  = "#F0C040"
PROTON_CREAM       = "#FFF8E7"
PROTON_BROWN       = "#8B4513"
PROTON_DARK        = "#0D2818"
PROTON_DARK_MID    = "#122B1E"
PROTON_DARK_CARD   = "#163022"
PROTON_BORDER      = "#1E4A2E"
PROTON_TEXT        = "#E8F5E9"
PROTON_TEXT_DIM    = "#8FBC8F"
PROTON_RED         = "#C0392B"
PROTON_ORANGE      = "#E67E22"

COLOR_SEQUENCE = [
    "#2E8B57", "#D4A017", "#52B788", "#F0C040",
    "#8B4513", "#4DB6AC", "#FF8A65", "#BA68C8",
    "#64B5F6", "#81C784", "#FFB74D", "#F06292",
]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'DM Sans', sans-serif", color=PROTON_TEXT, size=12),
    title_font=dict(family="'DM Sans', sans-serif", color=PROTON_TEXT, size=14),
    legend=dict(
        bgcolor="rgba(22,48,34,0.8)",
        bordercolor=PROTON_BORDER,
        borderwidth=1,
        font=dict(color=PROTON_TEXT, size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(46,139,87,0.12)",
        zerolinecolor="rgba(46,139,87,0.2)",
        tickfont=dict(color=PROTON_TEXT_DIM, size=11),
        linecolor=PROTON_BORDER,
    ),
    yaxis=dict(
        gridcolor="rgba(46,139,87,0.12)",
        zerolinecolor="rgba(46,139,87,0.2)",
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
