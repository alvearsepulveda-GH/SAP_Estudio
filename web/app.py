from __future__ import annotations

from os import getenv
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")
DATA_PATH = Path(
    getenv("SAP_ESTUDIO_EXCEL_PATH", BASE_DIR / "data" / "processed" / "resiliencia_financiera.xlsx")
)
TEMPLATE_DIR = BASE_DIR / "data" / "templates"

app = FastAPI(title="SAP Estudio - Resiliencia Financiera")
app.mount("/static", StaticFiles(directory=BASE_DIR / "web" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "web" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    cliente: str | None = None,
    pais: str | None = None,
    familia: str | None = None,
    periodo_desde: str | None = None,
    periodo_hasta: str | None = None,
) -> HTMLResponse:
    df, source_name = _load_resilience_data()
    df = _apply_filters(df, cliente, pais, familia, periodo_desde, periodo_hasta)
    records = _format_records(df)
    summary = _build_summary(df)
    product_chart = _build_product_chart(df)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "cliente": cliente or "",
            "pais": pais or "",
            "familia": familia or "",
            "periodo_desde": periodo_desde or "",
            "periodo_hasta": periodo_hasta or "",
            "source_name": source_name,
            "summary": summary,
            "product_chart": product_chart,
            "clientes": _unique_values(df, "nombre_cliente"),
            "paises": _unique_values(df, "pais"),
            "familias": _unique_values(df, "familia_producto"),
            "records": records,
            "columns": [
                "periodo",
                "pais",
                "sociedad_sap",
                "nombre_cliente",
                "familia_producto",
                "subfamilia_producto",
                "estado_ciclo_vida",
                "ventas_absorbentes",
                "costo_administracion_ventas",
                "ratio_absorcion",
            ],
        },
    )


def _load_resilience_data() -> tuple[pd.DataFrame, str]:
    if DATA_PATH.exists():
        return _load_from_excel(DATA_PATH), DATA_PATH.name

    return _load_from_templates(), "datos de ejemplo"


def _load_from_excel(path: Path) -> pd.DataFrame:
    clientes = pd.read_excel(path, sheet_name="clientes")
    productos = pd.read_excel(path, sheet_name="productos_equipos")
    celdas = pd.read_excel(path, sheet_name="celdas")
    base = pd.read_excel(path, sheet_name="base_mensual")
    return _merge_model(clientes, productos, celdas, base)


def _load_from_templates() -> pd.DataFrame:
    clientes = pd.read_csv(TEMPLATE_DIR / "clientes_jerarquia_template.csv")
    productos = pd.read_csv(TEMPLATE_DIR / "productos_equipos_jerarquia_template.csv")
    celdas = pd.read_csv(TEMPLATE_DIR / "celdas_cliente_producto_template.csv")
    base = pd.read_csv(TEMPLATE_DIR / "base_mensual_resiliencia_template.csv")
    return _merge_model(clientes, productos, celdas, base)


def _merge_model(
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    celdas: pd.DataFrame,
    base: pd.DataFrame,
) -> pd.DataFrame:
    df = base.merge(celdas, on="id_celda", how="left", suffixes=("", "_celda"))
    df = df.merge(clientes, on="id_cliente", how="left", suffixes=("", "_cliente"))
    df = df.merge(productos, on="id_producto_equipo", how="left", suffixes=("", "_producto"))
    df = _coalesce_duplicate_columns(df)
    if "costo_administracion_ventas" not in df.columns and "gav_asignado" in df.columns:
        df["costo_administracion_ventas"] = df["gav_asignado"]

    numeric_columns = [
        "ventas_repuestos",
        "ventas_servicios",
        "ventas_arriendos",
        "ventas_equipos_nuevos",
        "costo_administracion_ventas",
    ]
    for column in numeric_columns:
        if column not in df.columns:
            df[column] = 0
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["ventas_absorbentes"] = (
        df["ventas_repuestos"] + df["ventas_servicios"] + df["ventas_arriendos"]
    )
    df["ratio_absorcion"] = df.apply(
        lambda row: row["ventas_absorbentes"] / row["costo_administracion_ventas"]
        if row["costo_administracion_ventas"]
        else 0,
        axis=1,
    )
    return df


def _coalesce_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in list(df.columns):
        if column.endswith("_celda") or column.endswith("_cliente") or column.endswith("_producto"):
            base_column = column.rsplit("_", 1)[0]
            if base_column in df.columns:
                df[base_column] = df[base_column].combine_first(df[column])
                df = df.drop(columns=[column])
    return df


def _apply_filters(
    df: pd.DataFrame,
    cliente: str | None,
    pais: str | None,
    familia: str | None,
    periodo_desde: str | None,
    periodo_hasta: str | None,
) -> pd.DataFrame:
    filtered = df.copy()
    if cliente:
        mask = (
            filtered["nombre_cliente"].astype(str).str.contains(cliente, case=False, na=False)
            | filtered["codigo_cliente_sap"].astype(str).str.contains(cliente, case=False, na=False)
        )
        filtered = filtered[mask]
    if pais:
        filtered = filtered[filtered["pais"].astype(str).str.casefold() == pais.casefold()]
    if familia:
        filtered = filtered[
            filtered["familia_producto"].astype(str).str.casefold() == familia.casefold()
        ]
    if periodo_desde:
        filtered = filtered[filtered["periodo"].astype(str) >= periodo_desde]
    if periodo_hasta:
        filtered = filtered[filtered["periodo"].astype(str) <= periodo_hasta]
    return filtered.sort_values(["periodo", "nombre_cliente", "familia_producto"])


def _build_summary(df: pd.DataFrame) -> dict[str, str]:
    ventas_absorbentes = float(df["ventas_absorbentes"].sum()) if not df.empty else 0
    costo = float(df["costo_administracion_ventas"].sum()) if not df.empty else 0
    ratio = ventas_absorbentes / costo if costo else 0
    return {
        "clientes": f"{df['codigo_cliente_sap'].nunique():,.0f}",
        "celdas": f"{df['id_celda'].nunique():,.0f}",
        "ventas_absorbentes": _format_money(ventas_absorbentes),
        "ratio_absorcion": f"{ratio:.2f}",
    }


def _build_product_chart(df: pd.DataFrame) -> list[dict[str, str]]:
    if df.empty:
        return []

    grouped = (
        df.groupby("familia_producto", dropna=False)
        .agg(
            ventas_absorbentes=("ventas_absorbentes", "sum"),
            costo_administracion_ventas=("costo_administracion_ventas", "sum"),
            celdas=("id_celda", "nunique"),
        )
        .reset_index()
    )
    grouped["ratio_absorcion"] = grouped.apply(
        lambda row: row["ventas_absorbentes"] / row["costo_administracion_ventas"]
        if row["costo_administracion_ventas"]
        else 0,
        axis=1,
    )
    max_sales = grouped["ventas_absorbentes"].max() or 1
    grouped = grouped.sort_values("ventas_absorbentes", ascending=False)

    return [
        {
            "familia_producto": str(row["familia_producto"]),
            "ventas_absorbentes": _format_money(float(row["ventas_absorbentes"])),
            "ratio_absorcion": f"{float(row['ratio_absorcion']):.2f}",
            "celdas": f"{int(row['celdas']):,}".replace(",", "."),
            "width": f"{max(float(row['ventas_absorbentes']) / max_sales * 100, 3):.1f}%",
        }
        for _, row in grouped.iterrows()
    ]


def _format_records(df: pd.DataFrame) -> list[dict[str, object]]:
    visible = df.head(500).copy()
    visible["ventas_absorbentes"] = visible["ventas_absorbentes"].map(_format_money)
    visible["costo_administracion_ventas"] = visible["costo_administracion_ventas"].map(
        _format_money
    )
    visible["ratio_absorcion"] = visible["ratio_absorcion"].map(lambda value: f"{value:.2f}")
    return visible.to_dict(orient="records")


def _format_money(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def _unique_values(df: pd.DataFrame, column: str) -> list[str]:
    if column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())
