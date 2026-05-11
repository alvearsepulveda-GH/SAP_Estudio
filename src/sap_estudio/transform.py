from __future__ import annotations

import pandas as pd


def preparar_clientes(clientes: pd.DataFrame) -> pd.DataFrame:
    """Normaliza campos basicos de clientes para consumo web."""
    df = clientes.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    return df.drop_duplicates()


def preparar_facturas(facturas: pd.DataFrame) -> pd.DataFrame:
    """Normaliza facturas y calcula campos utiles para visualizacion."""
    df = facturas.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    for column in ["fecha_factura", "fecha_envio", "vencimiento"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    if "monto" in df.columns:
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce")

    return df


def unir_clientes_facturas(clientes: pd.DataFrame, facturas: pd.DataFrame) -> pd.DataFrame:
    """Une clientes y facturas usando una llave comun si esta disponible."""
    clientes_limpios = preparar_clientes(clientes)
    facturas_limpias = preparar_facturas(facturas)

    for key in ["cliente_id", "codigo_cliente", "rut_cliente"]:
        if key in clientes_limpios.columns and key in facturas_limpias.columns:
            return facturas_limpias.merge(clientes_limpios, on=key, how="left")

    return facturas_limpias
