from __future__ import annotations

from typing import Any

from sap_estudio.config import SapConfig


class SapConnectionUnavailable(RuntimeError):
    """Se lanza cuando no esta disponible el conector SAP."""


def create_connection(config: SapConfig) -> Any:
    """Crea una conexion RFC hacia SAP usando pyrfc.

    Requiere instalar la dependencia opcional `pyrfc` y contar con SAP NW RFC SDK
    configurado en el equipo.
    """
    try:
        from pyrfc import Connection
    except ImportError as exc:
        raise SapConnectionUnavailable(
            "No se encontro pyrfc. Instala el extra SAP y configura SAP NW RFC SDK."
        ) from exc

    return Connection(
        ashost=config.ashost,
        sysnr=config.sysnr,
        client=config.client,
        user=config.user,
        passwd=config.password,
        lang=config.lang,
    )
