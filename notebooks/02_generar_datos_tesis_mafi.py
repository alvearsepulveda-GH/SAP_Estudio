# %% [markdown]
# # Generacion de datos - Tesis MAFI USACH
#
# Este notebook permite ejecutar paso a paso la simulacion de datos para la
# tesis de resiliencia financiera.
#
# La logica base vive en `scripts/generate_resilience_simulation.py`, para
# mantener una sola fuente de verdad.

# %% [markdown]
# ## 1. Preparar entorno
#
# Ejecuta esta celda primero. Define rutas e importa las funciones del generador.

# %%
from pathlib import Path
from random import Random
import sys

import pandas as pd

PROJECT_DIR = Path.cwd().resolve()
if PROJECT_DIR.name == "notebooks":
    PROJECT_DIR = PROJECT_DIR.parent

sys.path.insert(0, str(PROJECT_DIR))

from scripts import generate_resilience_simulation as sim

PROJECT_DIR

# %% [markdown]
# ## 2. Parametros generales
#
# La simulacion cubre 2020-01 a 2025-12. Son 72 meses completos.

# %%
rng = Random(42)
periods = sim._periods()

periods[:3], periods[-3:], len(periods)

# %% [markdown]
# ## 3. Jerarquia de clientes
#
# Clientes simulados para Chile. Esta tabla representa la jerarquia de clientes:
# industria, grupo economico, cliente y faena.

# %%
clients = sim._clients()
clientes_df = pd.DataFrame([sim._client_row(client) for client in clients])
clientes_df

# %% [markdown]
# ## 4. Jerarquia de productos/equipos
#
# Incluye grupos de equipos, subfamilias, estado comercial y ciclo de vida.

# %%
products = sim._products()
productos_df = pd.DataFrame([sim._product_row(product) for product in products])
productos_df

# %% [markdown]
# ## 5. Celdas cliente-producto
#
# Cada celda cruza un cliente con un equipo/material. En estas celdas vive el RAPV.

# %%
cells = sim._cells(clients, products, rng)
celdas_df = pd.DataFrame(cells)

celdas_df.head(), celdas_df.shape

# %% [markdown]
# ## 6. GAV mensual
#
# Simula el gasto de administracion y ventas mensual. Luego se asigna
# proporcionalmente a cada celda.

# %%
gav = sim._gav_monthly(periods)
gav_df = pd.DataFrame(gav)

gav_df.head(), gav_df.tail()

# %% [markdown]
# ## 7. Facturacion y margen post-venta
#
# Esta es la tabla principal. Contiene ventas de equipos, repuestos, servicios,
# arriendos, margenes, GAV asignado, RAPV y DOS.

# %%
facts = sim._facts(periods, cells, clients, products, gav, rng)
base_mensual_df = pd.DataFrame(facts)

base_mensual_df.head()

# %%
relationship_cells = sim._relationship_cells(cells, facts)
celdas_relacion_df = pd.DataFrame(relationship_cells)

celdas_relacion_df.loc[
    :,
    [
        "id_celda",
        "nombre_cliente",
        "familia_producto",
        "subfamilia_producto",
        "facturacion_servicios_arriendos",
        "gav_mensual_prorrateado_familia",
        "margen_postventa_total",
        "rapv_periodo_total",
    ],
].head()

# %% [markdown]
# ## 8. Verificar calculo RAPV
#
# RAPV = margen_postventa / gav_asignado.

# %%
check_cols = [
    "periodo",
    "nombre_cliente",
    "familia_producto",
    "margen_postventa",
    "gav_asignado",
    "ratio_absorcion",
    "dos",
]

sample = base_mensual_df.loc[:, check_cols].head(10).copy()
sample["rapv_recalculado"] = sample["margen_postventa"] / sample["gav_asignado"]
sample["rapv_%"] = sample["rapv_recalculado"].map(lambda value: f"{value:.2%}")
sample

# %% [markdown]
# ## 9. Matriz cliente x grupo de equipos
#
# Eje Y: jerarquia/agrupacion de clientes. Eje X: grupos de productos/equipos.
# Cada celda muestra RAPV y DOS.

# %%
matrix = sim._matrix(cells, clients, products, facts)
matriz_df = pd.DataFrame(matrix)

matriz_df

# %% [markdown]
# ## 10. Resumen por grupo de productos
#
# Permite ver que familias aportan mas al margen post-venta, RAPV y DOS.

# %%
family_summary = sim._family_summary(facts)
familia_df = pd.DataFrame(family_summary)

familia_df

# %% [markdown]
# ## 11. Resumen por cliente
#
# Permite identificar clientes con mayor aporte y revisar si el aporte esta
# alineado con cobranza.

# %%
customer_summary = sim._customer_summary(facts)
cliente_resumen_df = pd.DataFrame(customer_summary)

cliente_resumen_df.head(12)

# %% [markdown]
# ## 12. Control de calidad de datos
#
# Validaciones simples antes de exportar.

# %%
quality = {
    "periodos": base_mensual_df["periodo"].nunique(),
    "clientes": base_mensual_df["codigo_cliente_sap"].nunique(),
    "familias_producto": base_mensual_df["familia_producto"].nunique(),
    "celdas": base_mensual_df["id_celda"].nunique(),
    "registros": len(base_mensual_df),
    "rapv_promedio_simple": base_mensual_df["ratio_absorcion"].mean(),
    "dos_promedio": base_mensual_df["dos"].mean(),
}

quality

# %% [markdown]
# ## 13. Exportar Excel completo
#
# Esta celda ejecuta el generador oficial y crea el Excel en `data/processed`
# y OneDrive.

# %%
sim.main()

# %% [markdown]
# ## 14. Rutas de salida
#
# Archivos generados por el script.

# %%
print("Local:", sim.LOCAL_FILE)
print("OneDrive:", sim.ONEDRIVE_FILE)
