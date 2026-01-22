# Momento3

Generador de reporte interactivo en HTML usando Python, Pandas y Plotly, con hoja de estilos personalizada y tabla interactiva (DataTables).

## Estructura del proyecto
- `Src/`
  - `generar_reporte.py`: carga el CSV, genera los gráficos (frecuencia, tendencia, distribución) y produce `reporte.html`.
  - `visualizacion.py`: helpers para crear las figuras Plotly.
  - `__init__.py`
- `Assets/`
  - `estilos.css`: estilos del reporte.
  - `script.js`: inicializa DataTables y renderiza los gráficos Plotly a partir del JSON embebido.
- `Data/`
  - `datos_limpios.csv`: datos de ejemplo/entrada.
- `reporte.html`: reporte generado listo para abrir en el navegador.
- `requirements.txt`: dependencias mínimas (ajusta según tus librerías reales).

## Requisitos
- Python 3.9+ (recomendado)
- Dependencias:
  - pandas
  - plotly
  - (opcional) cualquier otra que agregues a `requirements.txt`

Instalación rápida:
```bash
python -m pip install -r requirements.txt
```

## Uso
Desde la raíz del repo:
```bash
python Src/generar_reporte.py
```
Esto creará/actualizará `reporte.html`. Ábrelo en tu navegador (Ctrl+F5 para recargar sin caché).

## Personalización
- Datos: reemplaza `Data/datos_limpios.csv` por tu dataset. Ajusta las columnas de categoría/fecha/valor en `generar_reporte.py` (variables `COL_FRECUENCIA`, `COL_FECHA`, `COL_VALOR`).
- Estilos: modifica `Assets/estilos.css`.
- Lógica JS (DataTables/Plotly render): `Assets/script.js`.
- Plantilla: el HTML se genera dentro de `generar_reporte.py`; puedes editar el layout o secciones allí.

## Notas
- Evita subir `__pycache__` y archivos `.pyc` (ya incluido en `.gitignore`).
- Si quieres excluir CSV grandes/sensibles, ajústalo en `.gitignore`.
