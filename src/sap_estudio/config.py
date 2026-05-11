from __future__ import annotations

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class SapConfig:
    ashost: str
    sysnr: str
    client: str
    user: str
    password: str
    lang: str = "ES"


def load_sap_config() -> SapConfig:
    """Carga configuracion SAP desde variables de entorno o archivo .env."""
    load_dotenv()
    return SapConfig(
        ashost=_required_env("SAP_ASHOST"),
        sysnr=_required_env("SAP_SYSNR"),
        client=_required_env("SAP_CLIENT"),
        user=_required_env("SAP_USER"),
        password=_required_env("SAP_PASSWORD"),
        lang=getenv("SAP_LANG", "ES"),
    )


def _required_env(name: str) -> str:
    value = getenv(name)
    if not value:
        raise RuntimeError(f"Falta configurar la variable de entorno {name}")
    return value
