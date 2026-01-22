
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from visualizacion import graficar_frecuencia, graficar_tendencia_temporal, graficar_distribucion

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_DATOS = BASE_DIR / "Data" / "datos_limpios.csv"

COL_FRECUENCIA = "categoria"
COL_FECHA = "fecha"
COL_VALOR = "monto"
TOP_N = 10

print(f"📂 Cargando datos desde: {RUTA_DATOS}")
df = pd.read_csv(RUTA_DATOS)
if df.empty:
    print("❌ CSV vacío"); sys.exit(1)
print(f"✅ Datos: {len(df)} filas, {len(df.columns)} columnas: {list(df.columns)}")

# Genera gráficos (sin try/except para ver el error real)
json_frec = graficar_frecuencia(df, COL_FRECUENCIA, top_n=TOP_N, titulo=f"Top {TOP_N} elementos más frecuentes")
json_tend = graficar_tendencia_temporal(df, COL_FECHA, COL_VALOR, freq="D", modo="linea", titulo="Tendencia temporal diaria")
json_dist = graficar_distribucion(df, COL_VALOR, titulo=f"Distribución de {COL_VALOR}")

# Tabla
df_resumen = (
    df.groupby(COL_FRECUENCIA)[COL_VALOR]
    .agg(["sum", "mean", "count"])
    .reset_index()
    .sort_values("sum", ascending=False)
)
df_resumen.columns = [COL_FRECUENCIA.capitalize(), "Total", "Promedio", "Cantidad"]
tabla_html = df_resumen.to_html(index=False, classes="display compact stripe hover", table_id="tabla-datos", float_format="%.2f", border=0)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Reporte de Análisis</title>
  <link rel="stylesheet" href="Assets/estilos.css" />
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css" />
  <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
</head>
<body>
  <nav class="topbar">
    <div class="brand">PYDATAREPORT</div>
    <div class="nav-links">
      <a href="#resumen">Resumen</a>
      <a href="#frecuencia">Frecuencia</a>
      <a href="#tendencia">Tendencia</a>
      <a href="#distribucion">Distribución</a>
      <a href="#tabla">Tabla</a>
    </div>
    <button id="btn-top" class="ghost-btn">↑ Top</button>
  </nav>

  <main>
    <section id="resumen" class="section cards-grid">
      <article class="card stat"><p class="label">Total filas</p><h3>{len(df):,}</h3><p class="hint">Registros analizados</p></article>
      <article class="card stat"><p class="label">Columnas</p><h3>{len(df.columns)}</h3><p class="hint">Estructura del dataset</p></article>
      <article class="card stat"><p class="label">Rango de fechas</p><h3>{pd.to_datetime(df[COL_FECHA]).min().strftime('%Y-%m-%d') if COL_FECHA in df.columns else '-'} — {pd.to_datetime(df[COL_FECHA]).max().strftime('%Y-%m-%d') if COL_FECHA in df.columns else '-'}</h3><p class="hint">Columna: {COL_FECHA}</p></article>
      <article class="card stat"><p class="label">Suma de {COL_VALOR}</p><h3>{df[COL_VALOR].sum():,.2f}</h3><p class="hint">Métrica agregada</p></article>
    </section>

    <section id="frecuencia" class="section two-col">
      <div>
        <div class="section-header"><h2>🔝 Elementos más frecuentes</h2><span class="pill">Top {TOP_N}</span></div>
        <div class="card chart-card"><div id="chart-frec"></div></div>
      </div>
      <aside class="card side-info">
        <h4>Info rápida</h4>
        <ul>{"".join(f"<li>{cat}: {val} ({val/df[COL_FRECUENCIA].value_counts().sum()*100:,.1f}%)</li>" for cat,val in df[COL_FRECUENCIA].value_counts().head(TOP_N).items())}</ul>
        <p>Participación Top 1: <strong>{df[COL_FRECUENCIA].value_counts().iloc[0]/df[COL_FRECUENCIA].value_counts().sum()*100:,.1f}% del total</strong></p>
        <p>Hover para valores exactos. Orden ascendente para resaltar el top.</p>
        <p>Columna: <strong>{COL_FRECUENCIA}</strong></p>
      </aside>
    </section>

    <section id="tendencia" class="section two-col">
      <div>
        <div class="section-header"><h2>📈 Tendencia temporal</h2><span class="pill">Serie temporal</span></div>
        <div class="card chart-card"><div id="chart-tend"></div></div>
      </div>
      <aside class="card side-info">
        <h4>Tip</h4>
        <p>Usa zoom/brush para periodos específicos.</p>
        <p>Fecha: <strong>{COL_FECHA}</strong> · Valor: <strong>{COL_VALOR}</strong></p>
      </aside>
    </section>

    <section id="distribucion" class="section two-col">
      <div>
        <div class="section-header"><h2>📊 Distribución de valores</h2><span class="pill">Histograma</span></div>
        <div class="card chart-card"><div id="chart-dist"></div></div>
      </div>
      <aside class="card side-info">
        <h4>Lectura</h4>
        <p>Evalúa sesgos, colas y concentración.</p>
        <p>Columna: <strong>{COL_VALOR}</strong></p>
      </aside>
    </section>

    <section id="tabla" class="section">
      <div class="section-header"><h2>📋 Tabla de datos</h2><span class="pill">Interactiva</span></div>
      <div class="card table-card">{tabla_html}</div>
    </section>
  </main>

  <footer class="footer"><p>Generado con PYDATAREPORT | Python + Pandas + Plotly + DataTables</p></footer>

  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
  <script id="data-frec" type="application/json">{json_frec}</script>
  <script id="data-tend" type="application/json">{json_tend}</script>
  <script id="data-dist" type="application/json">{json_dist}</script>
  <script src="Assets/script.js"></script>
</body>
</html>
"""
output = BASE_DIR / "reporte.html"
output.write_text(html, encoding="utf-8")
print(f"\n✅ Reporte generado: {output}")
