# Bitacora - SAP Estudio

## Objetivo Conversado

El proyecto busca crear una conexion a SAP para ejecutar un SAPScript o consulta previamente creada, extraer una tabla llamada cliente y obtener las facturas enviadas a clientes durante el mes.

Luego, la informacion debe visualizarse en una pagina web para que un usuario pueda visitar clientes y revisar que documentos ha recibido cada uno.

## Alcance Inicial

Se propone construir el proyecto en capas:

1. Conexion segura a SAP.
2. Ejecucion de consulta o script SAP.
3. Extraccion de clientes.
4. Extraccion de facturas mensuales.
5. Limpieza y union de datos.
6. Visualizacion web.

## Pendientes por Definir

- Tipo exacto de conexion disponible: RFC, SAP GUI scripting, OData, archivo exportado u otro.
- Nombre tecnico real de la tabla de clientes.
- Nombre tecnico real de la tabla de facturas.
- Campos obligatorios para la pagina web.
- Si el usuario consultara por cliente, vendedor, sucursal, fecha o estado del documento.
- Periodicidad de actualizacion: manual, diaria, mensual o bajo demanda.

## Nota de Seguridad

Las credenciales de SAP no deben subirse a GitHub. Deben permanecer en `.env` local o en variables de entorno.
