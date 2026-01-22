
import pandas as pd
import plotly.express as px

AXIS_COLOR = "#e5e7eb"
TEXT_COLOR = "#f8fafc"

def _tune_axes(fig, gridcolor="rgba(255,255,255,0.18)"):
    fig.update_xaxes(
        tickfont=dict(color=AXIS_COLOR),
        title_font=dict(color=AXIS_COLOR),
        gridcolor=gridcolor,
        zeroline=False,
    )
    fig.update_yaxes(
        tickfont=dict(color=AXIS_COLOR),
        title_font=dict(color=AXIS_COLOR),
    )

def graficar_frecuencia(df: pd.DataFrame, columna: str, top_n: int = 10, titulo: str = "") -> str:
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame")
    conteo = df[columna].value_counts().head(top_n)
    data = conteo.reset_index()
    data.columns = [columna, "Frecuencia"]
    fig = px.bar(
        data, x="Frecuencia", y=columna, orientation="h",
        title=titulo or f"Top {top_n} de {columna}",
        color="Frecuencia", color_continuous_scale="Blues",
        height=360, labels={columna: columna.capitalize()},
        text="Frecuencia",
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="<b>%{x:.0f}</b>",
        textfont=dict(color=TEXT_COLOR, size=13),
        marker_line_color="#0b1224",
        marker_line_width=1.2,
        cliponaxis=False,
        opacity=0.93,
    )
    _tune_axes(fig)
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(categoryorder="total ascending"),
        title_font_color=AXIS_COLOR,
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=AXIS_COLOR, size=13),
    )
    return fig.to_json()

def graficar_tendencia_temporal(df: pd.DataFrame, columna_fecha: str, columna_valor: str, freq: str = "D", modo: str = "linea", titulo: str = "") -> str:
    if columna_fecha not in df.columns or columna_valor not in df.columns:
        raise ValueError("Columnas indicadas no existen en el DataFrame")
    tmp = df.copy()
    tmp[columna_fecha] = pd.to_datetime(tmp[columna_fecha])
    serie = tmp.set_index(columna_fecha)[columna_valor].resample(freq).sum().reset_index()
    fig = px.area(
        serie, x=columna_fecha, y=columna_valor,
        title=titulo or f"Tendencia de {columna_valor} ({freq})",
        markers=True, height=360,
    )
    _tune_axes(fig, gridcolor="rgba(255,255,255,0.12)")
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=AXIS_COLOR, size=13),
        title_font_color=AXIS_COLOR,
    )
    return fig.to_json()

def graficar_distribucion(df: pd.DataFrame, columna: str, titulo: str = "") -> str:
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame")
    fig = px.histogram(
        df, x=columna, nbins=30,
        title=titulo or f"Distribución de {columna}",
        height=360, color_discrete_sequence=["#7c3aed"],
    )
    _tune_axes(fig, gridcolor="rgba(255,255,255,0.12)")
    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=AXIS_COLOR, size=13),
        title_font_color=AXIS_COLOR,
    )
    return fig.to_json()
