# io/__init__.py
from .merge_peak_tables import merge_peak_tables
from .update_xlsx_db import update_xlsx_db

# Alias de compatibilidad (nombre anterior de la funcion).
merge_channels = merge_peak_tables

__all__ = ["merge_peak_tables", "merge_channels", "update_xlsx_db"]
