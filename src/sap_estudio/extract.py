from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def extract_clientes(connection: Any, table_name: str = "CLIENTE") -> pd.DataFrame:
    """Extrae la tabla de clientes desde SAP.

    Esta funcion queda como punto unico para adaptar el nombre real de tabla,
    vista, RFC o SAPScript definido por el equipo.
    """
    return _read_sap_table(connection, table_name)


def extract_facturas_mes(connection: Any, year: int, month: int, table_name: str) -> pd.DataFrame:
    """Extrae facturas enviadas a clientes para un mes dado."""
    df = _read_sap_table(connection, table_name)

    if "fecha_factura" in df.columns:
        fecha = pd.to_datetime(df["fecha_factura"], errors="coerce")
        df = df[(fecha.dt.year == year) & (fecha.dt.month == month)]

    return df


def save_raw_extract(df: pd.DataFrame, output_path: str | Path) -> None:
    """Guarda una extraccion original en CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _read_sap_table(connection: Any, table_name: str) -> pd.DataFrame:
    """Lee una tabla SAP mediante RFC_READ_TABLE.

    Puede requerir ajustes segun permisos, volumen de datos, campos esperados
    y restricciones del sistema SAP disponible.
    """
    result = connection.call("RFC_READ_TABLE", QUERY_TABLE=table_name, DELIMITER="|")
    fields = [field["FIELDNAME"] for field in result.get("FIELDS", [])]
    rows = [row["WA"].split("|") for row in result.get("DATA", [])]
    return pd.DataFrame(rows, columns=fields)
