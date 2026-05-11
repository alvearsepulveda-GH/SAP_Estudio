# SAP Estudio

Proyecto para conectar con SAP, ejecutar una consulta previamente definida, extraer informacion de clientes y facturas enviadas durante el mes, y visualizar los documentos en una pagina web para apoyar la visita y gestion con clientes.

## Objetivo

Construir un flujo reproducible que permita:

1. Conectarse a SAP de forma segura.
2. Ejecutar un SAPScript o consulta ya existente.
3. Extraer una tabla de clientes.
4. Extraer facturas enviadas a clientes durante un mes.
5. Transformar y validar la informacion.
6. Publicar una vista web simple para consulta de documentos por cliente.

## Flujo Propuesto

```text
SAP
  -> script o consulta existente
  -> extraccion clientes
  -> extraccion facturas del mes
  -> procesamiento local
  -> base/tablas preparadas
  -> pagina web de consulta
```

## Estructura

```text
data/
  raw/          datos originales extraidos desde SAP
  processed/    datos limpios listos para visualizar
docs/           bitacora, decisiones y documentacion funcional
notebooks/      exploracion y pruebas
reports/        salidas y figuras
src/            codigo principal del proyecto
tests/          pruebas unitarias
web/            aplicacion web
```

## Componentes

- `src/sap_estudio/config.py`: carga de configuracion y variables de entorno.
- `src/sap_estudio/sap_client.py`: conexion con SAP.
- `src/sap_estudio/extract.py`: ejecucion de consultas y extraccion de datos.
- `src/sap_estudio/transform.py`: limpieza y preparacion de clientes/facturas.
- `web/app.py`: aplicacion web para consultar documentos por cliente.

## Seguridad

Las credenciales de SAP no deben guardarse en Git. Deben manejarse mediante un archivo `.env` local o variables de entorno.

Ejemplo de variables esperadas:

```bash
SAP_ASHOST=
SAP_SYSNR=
SAP_CLIENT=
SAP_USER=
SAP_PASSWORD=
SAP_LANG=ES
```

## Estado Actual

Proyecto inicializado. Aun falta definir:

- Metodo exacto de conexion a SAP.
- Nombre tecnico del SAPScript, transaccion, RFC o consulta.
- Estructura de la tabla de clientes.
- Estructura de la tabla de facturas.
- Filtros del mes de consulta.
- Campos que vera el usuario en la pagina web.
