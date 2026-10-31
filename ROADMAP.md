# ROADMAP — chroma_tool_py

Guía de desarrollo para empaquetar y publicar el proyecto. Se basa en una revisión completa del repo (estructura, calidad de código y UI).

**Estado:** base funcional con datos reales de ChromNAV (~1800 líneas), todavía con aspecto de colección de scripts. Antes de publicar hay que resolver los bloqueantes de la Etapa 1.

> Decisión: **no** se usará `.github/` (sin CI/CD ni workflows de GitHub). Las pruebas y la publicación a PyPI se ejecutan en local.

---

## Etapa 1 — Bloqueantes antes de publicar

### 1.1 Datos y rutas personales
- [x] Quitar rutas personales: `utils/chroma_corrector.py:142,147` (rutas absolutas locales)
- [x] Decidir si `data/DLLME_Chromatograms/` (~12 MB, muestras reales trackeadas) se puede publicar. **Decision del usuario: se publica** como dataset de ejemplo, por lo que no hace falta limpiar el historial por este motivo. (Si se hubiera decidido no publicarlo, habria que limpiar el historial con `git filter-repo`.)
- [x] Verificar que `data/GWR_project/` y `data/client_images/` (ignorados) nunca se suban.
- [ ] Auditar el historial buscando credenciales (`gitleaks`, `git log -p -S`). En el código no se encontró ninguna.
- [ ] Crear `data/sample/` con un cromatograma sintético pequeño (<100 KB).

### 1.2 Imports y dependencias rotas
- [x] `classes/chroma_visualizer.py:6`: `from utils import info, extract` → import absoluto del paquete.
- [x] `pyproject.toml`: añadir numpy, scipy y matplotlib (hoy solo declara pandas, openpyxl y xlrd). `pybeads` como extra opcional.
- [x] Añadir `__init__.py` en `cli/` y `processing/` (sin ellos los entry points fallan tras `pip install`).
- [x] `io/__init__.py` sombrea el submódulo `merge_channels` con la función homónima; `cli/process_chromnav_batch.py` depende de ello. Corregir ambos.
- [x] `utils/chroma_corrector.py` ejecuta código con rutas a nivel de módulo: mover a `if __name__ == "__main__"` o eliminar.

### 1.3 Duplicados y obsoletos
- [x] Renombrar los dos `merge_channels.py`: `io/merge_pda_channels.py` (une canales y grafica) y `io/merge_peak_tables.py` (une Excel de picos).
- [x] Borrar `utils/peak_finder copy.py` (no importable, parámetros distintos).
- [x] Borrar `obsolete/`, `dev/`, `test/` (scripts manuales, no pytest) y `__pycache__`.
- [x] `io/` y `utils/` se solapan: redistribuir el contenido.

### 1.4 Bugs de código
- [x] `Chromatogram.create_from_fl`: `removesuffix("(01).csv")` sobre un `stem` nunca recorta nada.
- [x] `Chromatogram.create_from_pda`: cabecera fija de 11 líneas (`i < 11`, `i > 11`), sin `encoding`. Leer la cabecera por clave.
- [x] `add_fl` guarda un dict y `create_from_fl` un DataFrame: unificar el tipo de `FL_DATA`.
- [x] `Sequence.execute` está mal indentado dentro de `__init__` (código muerto).
- [x] `assert type(x) is str` en `Chromatogram`, `Analyte` y `Sequence`: usar `isinstance` + `TypeError`.
- [x] `io/merge_pda_channels.py` (antes `utils/merge_channels.py`): corta los últimos 4 caracteres del nombre y asigna con `.loc` sobre un slice (`SettingWithCopyWarning`).
- [x] `processing/calibration_curve_params.py`: rango fijo `H2:I4` y reescritura del mismo Excel en modo append (falla si la hoja existe).

### 1.5 Metadatos y documentación mínima
- [x] `pyproject.toml`: descripción real, `readme`, `requires-python = ">=3.10"`, licencia, autores, keywords, classifiers, `[project.urls]`.
- [x] Reemplazar `requirements.txt` (UTF-16, pins de 2023) por extras en `pyproject.toml`.
- [x] LICENSE con nombre completo y año 2023–2026.
- [x] README: corregir la ruta del logo (`Images/logo.png` no existe; está en `data/others/logo.png`), quitar referencias a archivos que ya no existen, añadir instalación y ejemplos de CLI.
- [x] `.gitignore`: añadir `dist/`, `build/`, `*.egg-info`, `.venv`, `.vscode`, `.idea`, `*.xlsx`. Resolver `.pylintrc` y `OOP.md` (movido a `docs/design.md`).
- [ ] `.gitignore`: ignorar `data/*` salvo `data/sample/` y `data/DLLME_Chromatograms/`. Resolver `TASKS.md` (ignorado pero trackeado).
- [ ] Optimizar `assets/logo.png` (3.1 MB) y revisar `data/others/COSMOS_bar_plot.png`, que sigue trackeado.

---

## Etapa 2 — Estructura objetivo del repo

```
chroma_tool_py/
├─ src/chroma_tool_py/
│  ├─ __init__.py               # __version__ + API pública (__all__)
│  ├─ classes/                  # Analyte, Chromatogram, Sequence
│  ├─ io/                       # readers, rename, merge_pda_channels, merge_peak_tables, update_xlsx_db
│  ├─ processing/               # peak_finder, baseline (pybeads opcional), calibration
│  ├─ display/                  # chroma_plot, peaks_plot (devuelven Figure)
│  ├─ gui/                      # chroma_visualizer (tkinter, opcional) y/o app Streamlit
│  ├─ cli/                      # plot_batch_pda, plot_batch_fl, process_chromnav_batch, rename
│  └─ py.typed
├─ tests/                       # pytest con datos sintéticos
├─ examples/                    # 01_plot_pda.py, 02_calibration.py, quickstart.ipynb
├─ data/sample/                 # cromatograma sintético (<100 KB)
├─ docs/
│  ├─ index.md
│  ├─ installation.md
│  ├─ chromnav-format.md        # cómo exportar y qué formato espera
│  ├─ cli.md
│  ├─ api.md
│  ├─ design.md                 # de OOP.md, si aporta
│  └─ roadmap.md                # opcional, enlace a este archivo
├─ assets/                      # logo, capturas, GIF de demo
├─ README.md (EN) + README.es.md
├─ ROADMAP.md, CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CITATION.cff
└─ LICENSE, pyproject.toml, .gitignore
```

Sin `.github/`. Eliminar: `obsolete/`, `dev/`, `test/`, `src/README.md`, `requirements.txt`, `peak_finder copy.py`.

---

## Etapa 3 — Calidad de la librería

- [ ] `display/*` debe devolver `Figure` (con `save_path` opcional) y no llamar a `plt.show()`/`plt.close()` internamente. Requisito para cualquier UI.
- [ ] Reemplazar `print` por `logging` en la librería (~107 `print`; dejarlos solo en los CLIs).
- [ ] Excepciones propias (`ChromNAVFormatError`); los CLIs no deben capturar `Exception` genérica (`plot_batch_pda.py:85`, `plot_batch_fl.py:40`).
- [ ] Type hints y docstrings consistentes (hoy mezclan inglés/español con erratas: "wavelenth", "chromaotgram").
- [ ] Parámetros hardcodeados → argumentos: `peak_finder` (`height=10000`, `threshold=1`), `pda_contour` en CLI (`y_max=400`, `z_min=-10000`, `z_max=530000`).
- [ ] Tests pytest con datos sintéticos y `tmp_path`; objetivo inicial ≥60 % de cobertura. `ruff` para lint y estilo (ejecución local).
- [ ] CLIs: mantener los 3 entry points, añadir `chroma-rename`, o un comando único `chroma-tool` con subcomandos. Todos con `--help` y probados.

---

## Etapa 4 — Mejoras de arquitectura y funcionalidad

**Medio plazo**
- [ ] `Chromatogram` como `@dataclass` con `time`, `wavelengths` e `intensity` ya parseados; tipos `PDA`/`FL` explícitos.
- [ ] Eliminar los registros globales `Chromatogram.all`, `Analyte.all`, `Sequence.all` (estado compartido, fugas de memoria en batch).
- [ ] Parser robusto de ChromNAV con un único punto de entrada (`io/readers.py`).
- [ ] `peak_finder` parametrizable, con integración de área (trapecio, baseline) y resultado en dataclass `Peak`.
- [ ] Módulo `calibration`: regresión lineal (pendiente, intercepto, R², LOD/LOQ) con `scipy.stats.linregress`, en lugar de leer celdas de Excel.

**Largo plazo**
- [ ] Biblioteca de espectros para `Analyte` (identificación por coincidencia espectral).
- [ ] `Sequence` como pipeline ejecutable.
- [ ] Corrección de baseline.
- [ ] Exportadores CSV / Excel / PDF.

---

## Etapa 5 — UI

Recomendación: **Streamlit + Plotly**. Demo online gratuita enlazable desde LinkedIn e interactividad con poco esfuerzo. Depende de que `display/*` ya devuelva figuras (Etapa 3).

| Opción | Pros | Contras |
|---|---|---|
| **Streamlit + Plotly** | Rápida; demo online; `file_uploader` | Re-ejecuta el script en cada interacción; selección de picos por clic limitada |
| Dash/Plotly | Clic en gráfico, callbacks potentes | Más código y curva de aprendizaje |
| Gradio | Aún más simple | Pobre para flujos de varios pasos |
| PyQt/PySide | App nativa | Distribución pesada, no se comparte con un enlace |
| Jupyter widgets | Ideal para el notebook | No es una app |
| FastAPI + frontend | Escalable | Sobredimensionado |

**Flujo de pantallas:**
1. **Cargar:** PDA `.txt`, FL `.csv`, tablas de picos, o datos de ejemplo.
2. **Cromatogramas:** muestra, longitudes de onda; pestañas 2D / contorno / espectro; overlay de réplicas.
3. **Picos:** sliders de altura, prominencia y distancia; marcadores; tabla de tR, altura y área.
4. **Calibración:** tabla concentración vs área (`st.data_editor`), recta, R², LOD/LOQ, predicción de una muestra desconocida.
5. **Exportar:** Excel por analito (reutiliza `utils/excel.py` y `io/update_xlsx_db.py`), PNG/HTML, reporte.

Extra: `examples/quickstart.ipynb` como segundo entregable.

---

## Etapa 6 — Publicación

- [ ] Verificar que el nombre esté libre en PyPI.
- [ ] `python -m build` + `twine check dist/*`; instalar en un venv limpio; probar en TestPyPI y luego PyPI (manual, sin GitHub Actions).
- [ ] `CHANGELOG.md` (Keep a Changelog) con 0.1.0; `CONTRIBUTING.md`; `CODE_OF_CONDUCT.md`; `CITATION.cff`.
- [ ] README en inglés con badges (PyPI, licencia), instalación, quickstart de CLI, imagen de ejemplo y nota de formato ChromNAV/JASCO; sección Roadmap que enlaza a este archivo.

### Material para LinkedIn
- [ ] GIF de 15–20 s: subir archivo → mover slider de picos → curva de calibración → descargar Excel.
- [ ] Imagen de portada: contorno o superficie PDA (`pda_surface`) + logo.
- [ ] Demo online (Streamlit Cloud) y notebook ejecutado con salidas visibles.
- [ ] Texto del post: problema (ChromNAV exporta un canal por archivo; flujo manual en Excel), solución (pipeline en Python) y resultado cuantificable ("de N horas a 2 minutos por batch"). Destacar que es una herramienta de un químico analítico que programa.

---

## Orden de trabajo

1. Decidir sobre `data/DLLME_Chromatograms/` y auditar el historial.
2. Limpiar el repo (Etapa 1.1–1.3) y reorganizar según la Etapa 2.
3. Arreglar `pyproject.toml`, imports y bugs (1.2, 1.4, 1.5).
4. Etapa 3: figuras, logging, tests.
5. Docs y README.
6. Etapa 4 (lo imprescindible) y Etapa 5: UI y GIF.
7. Etapa 6: TestPyPI → PyPI → post.
