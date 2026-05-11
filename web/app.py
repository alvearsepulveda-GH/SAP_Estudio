from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "facturas_clientes.csv"

app = FastAPI(title="SAP Estudio")
app.mount("/static", StaticFiles(directory=BASE_DIR / "web" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "web" / "templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, cliente: str | None = None) -> HTMLResponse:
    df = _load_data()

    if cliente and "cliente" in df.columns:
        df = df[df["cliente"].astype(str).str.contains(cliente, case=False, na=False)]

    clientes = []
    if "cliente" in df.columns:
        clientes = sorted(df["cliente"].dropna().astype(str).unique().tolist())

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cliente": cliente or "",
            "clientes": clientes,
            "facturas": df.head(500).to_dict(orient="records"),
            "columns": df.columns.tolist(),
        },
    )


def _load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    return pd.DataFrame(
        [
            {
                "cliente": "Cliente ejemplo",
                "documento": "FAC-0001",
                "fecha_envio": "2026-05-10",
                "monto": 100000,
                "estado": "Enviado",
            }
        ]
    )
