# chroma_tool_py

Herramientas en Python para cargar, graficar y postprocesar cromatogramas HPLC-DAD (PDA) y de
fluorescencia (FL) exportados desde JASCO **ChromNAV**.

ChromNAV exporta un canal por archivo y unir todo manualmente en Excel es lento.
`chroma_tool_py` lee las exportaciones, crea objetos `Chromatogram` y ofrece tres comandos
(`plot-batch-pda`, `plot-batch-fl`, `process-chromnav-batch`) para procesar lotes completos.

## Instalacion

```bash
pip install git+https://github.com/marcovillegaz/chroma_tool_py.git
```

Desde un clon del repositorio: `pip install -e ".[dev]"`. Extra opcional para correccion de
linea base: `.[baseline]`.

La documentacion completa esta en ingles: [README.md](README.md) y [docs/index.md](docs/index.md).

> ChromNAV es un producto de JASCO Corporation. Este proyecto es independiente y no esta
> afiliado ni respaldado por JASCO; la marca ChromNAV del logo solo indica compatibilidad
> con su formato de exportacion.
