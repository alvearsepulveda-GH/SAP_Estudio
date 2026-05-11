import pandas as pd

from sap_estudio.transform import unir_clientes_facturas


def test_unir_clientes_facturas_por_cliente_id():
    clientes = pd.DataFrame(
        {
            "cliente_id": ["1"],
            "cliente": ["Cliente ejemplo"],
        }
    )
    facturas = pd.DataFrame(
        {
            "cliente_id": ["1"],
            "documento": ["FAC-0001"],
        }
    )

    result = unir_clientes_facturas(clientes, facturas)

    assert result.loc[0, "cliente"] == "Cliente ejemplo"
