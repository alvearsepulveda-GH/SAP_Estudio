# Plan de Trabajo - Integracion ECC, SAP BTP y SAP Estudio

Fecha: 2026-05-11

## 1. Antecedente usado como referencia

Se reviso el documento:

```text
ETF Proyecto Minera del Sol.docx
```

El documento describe una integracion 2024 entre ECC y Ariba, con elementos tecnicos que sirven como referencia para este proyecto:

- Parametros y rangos en `TVARVC`.
- Clases ABAP para encapsular la logica de negocio.
- Servicios/proxies inbound y outbound.
- Programas de control y programas monitor.
- Modulos de funcion.
- Clase de mensajes.
- Objetos de diccionario.
- Tablas Z de log y tracking.
- Jobs de fondo para ejecucion periodica.
- Integracion mediante CPI/SAP Integration Suite.

Para `SAP_Estudio`, no se copiara la solucion Ariba, pero si se usara el mismo criterio de arquitectura: separar configuracion, extraccion, servicio, log, monitoreo y consumo externo.

## 2. Objetivo del proyecto SAP Estudio

Construir una integracion para recuperar datos desde SAP ECC y dejarlos disponibles para una aplicacion externa que permita consultar clientes y documentos/facturas enviados.

Flujo objetivo:

```text
SAP ECC
  -> objetos Z de lectura y servicio
  -> Web Service SOAP / WSDL
  -> SAP BTP / Cloud Connector / Destination
  -> programa Python SAP_Estudio
  -> datos raw y processed
  -> aplicacion web de consulta
```

## 3. Principios de diseno tomados del proyecto ECC-Ariba

### 3.1 Parametrizar antes que dejar valores fijos

Usar `TVARVC` para parametros funcionales y tecnicos, por ejemplo:

```text
ZSAP_ESTUDIO_*
ZSAP_ESTUDIO_SOCIEDAD
ZSAP_ESTUDIO_ORG_VENTA
ZSAP_ESTUDIO_CLASE_FACTURA
ZSAP_ESTUDIO_CLIENTE
ZSAP_ESTUDIO_DIAS_CONSULTA
```

Esto evita dejar filtros fijos dentro del codigo ABAP.

### 3.2 Separar responsabilidades

La solucion deberia separar:

- Lectura de parametros.
- Obtencion de clientes.
- Obtencion de facturas/documentos.
- Armado de respuesta del servicio.
- Registro de log.
- Manejo de errores.
- Monitoreo.

### 3.3 Dejar trazabilidad

Igual que en el proyecto ECC-Ariba, conviene crear tablas de log/tracking para registrar:

- Fecha y hora de consulta.
- Usuario o sistema consumidor.
- Rango de fechas solicitado.
- Cantidad de clientes retornados.
- Cantidad de facturas retornadas.
- Estado de ejecucion.
- Mensaje de error, si aplica.

### 3.4 Tener monitor funcional

Crear un programa monitor permite revisar ejecuciones sin depender solo de logs tecnicos.

## 4. Fase ECC - Objetos propuestos

### 4.1 Objetos diccionario en SE11

#### Estructuras

```text
ZST_SAP_ESTUDIO_CLIENTE
ZST_SAP_ESTUDIO_FACTURA
ZST_SAP_ESTUDIO_RESPUESTA
ZST_SAP_ESTUDIO_MENSAJE
```

#### Tipos tabla

```text
ZTT_SAP_ESTUDIO_CLIENTE
ZTT_SAP_ESTUDIO_FACTURA
ZTT_SAP_ESTUDIO_MENSAJE
```

#### Tablas Z de log

```text
ZSAP_EST_LOG_H
ZSAP_EST_LOG_D
```

Uso sugerido:

```text
ZSAP_EST_LOG_H  Cabecera de ejecucion
ZSAP_EST_LOG_D  Detalle de mensajes, errores o advertencias
```

### 4.2 Campos sugeridos para cliente

```text
MANDT
KUNNR
NAME1
STCD1
ORT01
REGIO
LAND1
VKORG
VTWEG
SPART
```

Para evitar errores iniciales en `SE11`, se puede usar `LIKE` contra tablas estandar:

```text
KUNNR  LIKE KNA1-KUNNR
NAME1  LIKE KNA1-NAME1
STCD1  LIKE KNA1-STCD1
ORT01  LIKE KNA1-ORT01
REGIO  LIKE KNA1-REGIO
LAND1  LIKE KNA1-LAND1
VKORG  LIKE KNVV-VKORG
VTWEG  LIKE KNVV-VTWEG
SPART  LIKE KNVV-SPART
```

### 4.3 Campos sugeridos para factura/documento

```text
VBELN
FKDAT
KUNRG
KUNAG
NETWR
WAERK
VKORG
VTWEG
SPART
ERNAM
ERDAT
```

Referencias posibles:

```text
VBELN  LIKE VBRK-VBELN
FKDAT  LIKE VBRK-FKDAT
KUNRG  LIKE VBRK-KUNRG
KUNAG  LIKE VBRK-KUNAG
NETWR  LIKE VBRK-NETWR
WAERK  LIKE VBRK-WAERK
VKORG  LIKE VBRK-VKORG
VTWEG  LIKE VBRK-VTWEG
SPART  LIKE VBRK-SPART
ERNAM  LIKE VBRK-ERNAM
ERDAT  LIKE VBRK-ERDAT
```

## 5. Fase ECC - Logica ABAP

### 5.1 Clase de parametros

Crear una clase reutilizable para leer `TVARVC`, inspirada en el antecedente ECC-Ariba.

Nombre sugerido:

```text
ZCL_SAP_ESTUDIO_TVARVC
```

Responsabilidad:

- Leer parametros por patron `ZSAP_ESTUDIO_*`.
- Entregar rangos para filtros.
- Centralizar configuracion funcional.

### 5.2 Clase principal de servicio

Nombre sugerido:

```text
ZCL_SAP_ESTUDIO_DATOS
```

Metodos sugeridos:

```text
GET_CLIENTES
GET_FACTURAS
GET_DATOS
VALIDAR_ENTRADA
REGISTRAR_LOG
```

### 5.3 Function Module remoto

Nombre sugerido:

```text
ZFM_SAP_ESTUDIO_DATOS
```

Debe estar marcado como:

```text
Remote-Enabled Module
```

Parametros sugeridos:

```text
IMPORTING
  IV_FECHA_DESDE
  IV_FECHA_HASTA
  IV_CLIENTE
  IV_SOCIEDAD
  IV_ORG_VENTA

EXPORTING
  ET_CLIENTES
  ET_FACTURAS
  ET_MENSAJES
```

### 5.4 Clase de mensajes

Crear clase de mensajes:

```text
ZSAP_ESTUDIO
```

Mensajes sugeridos:

```text
001 Consulta ejecutada correctamente
002 Fecha desde es obligatoria
003 Fecha hasta es obligatoria
004 Rango de fechas invalido
005 Sin datos para los filtros indicados
006 Error al consultar clientes
007 Error al consultar facturas
008 Error al registrar log
```

## 6. Fase ECC - Servicio SOAP / WSDL

### 6.1 Crear Web Service

Exponer `ZFM_SAP_ESTUDIO_DATOS` como Web Service SOAP.

Flujo:

```text
SE37
  -> Function Module remoto
  -> crear Service Definition / Web Service
  -> SOAMANAGER
  -> crear binding
  -> activar endpoint
  -> obtener WSDL
```

### 6.2 Validaciones previas

Antes de pasar a BTP:

- Probar el Function Module en `SE37`.
- Probar el endpoint desde `SOAMANAGER`.
- Validar usuario tecnico.
- Validar autorizaciones.
- Validar HTTPS.
- Obtener URL WSDL.

## 7. Fase SAP BTP

### 7.1 Cloud Connector

Configurar SAP Cloud Connector entre SAP BTP y ECC.

Tareas:

```text
1. Conectar Cloud Connector al subaccount BTP.
2. Crear mapping del sistema ECC.
3. Definir host virtual.
4. Exponer solo paths necesarios.
```

Path probable:

```text
/sap/bc/srt/
```

### 7.2 Destination

Crear Destination en BTP:

```text
Name: ECC_SAP_ESTUDIO
Type: HTTP
Proxy Type: OnPremise
Authentication: BasicAuthentication o mecanismo definido por Basis
URL: host virtual del ECC
```

### 7.3 Prueba de conectividad

Validar:

- Connection Check de la Destination.
- Acceso al WSDL.
- Acceso al endpoint SOAP.
- Respuesta con usuario tecnico.

## 8. Fase programa Python SAP_Estudio

### 8.1 Dependencias

Agregar cliente SOAP:

```text
zeep
requests
```

### 8.2 Modulos propuestos

```text
src/sap_estudio/soap_client.py
src/sap_estudio/btp_destination.py
src/sap_estudio/extract.py
src/sap_estudio/transform.py
```

### 8.3 Flujo Python

```text
1. Leer configuracion.
2. Obtener URL WSDL o endpoint.
3. Llamar servicio SOAP.
4. Convertir respuesta a DataFrame.
5. Guardar raw.
6. Transformar.
7. Guardar processed.
8. Mostrar en web.
```

### 8.4 Ejemplo conceptual

```python
from zeep import Client

client = Client(wsdl="URL_DEL_WSDL")

response = client.service.ZFM_SAP_ESTUDIO_DATOS(
    IV_FECHA_DESDE="2026-05-01",
    IV_FECHA_HASTA="2026-05-31",
    IV_CLIENTE="",
    IV_SOCIEDAD="",
    IV_ORG_VENTA="",
)
```

## 9. Fase monitoreo y operacion

### 9.1 Monitor ECC

Crear programa monitor:

```text
ZPR_SAP_ESTUDIO_MON
```

Debe permitir:

- Consultar logs por fecha.
- Ver estado de ejecuciones.
- Ver parametros usados.
- Ver cantidad de registros.
- Ver errores.

### 9.2 Job de fondo

Si la extraccion sera periodica, crear job:

```text
ZJOB_SAP_ESTUDIO_DATOS
```

Frecuencia sugerida:

```text
Diaria o mensual, segun necesidad del negocio.
```

## 10. Entregables sugeridos

### ECC

- Estructuras `ZST_*`.
- Tipos tabla `ZTT_*`.
- Tablas log `ZSAP_EST_LOG_*`.
- Clase parametros `ZCL_SAP_ESTUDIO_TVARVC`.
- Clase negocio `ZCL_SAP_ESTUDIO_DATOS`.
- Function Module `ZFM_SAP_ESTUDIO_DATOS`.
- Clase mensajes `ZSAP_ESTUDIO`.
- Web Service SOAP.
- WSDL.
- Programa monitor.

### SAP BTP

- Cloud Connector configurado.
- Destination `ECC_SAP_ESTUDIO`.
- Prueba de conectividad documentada.

### Python

- Cliente SOAP.
- Transformacion de respuesta.
- Persistencia en `data/raw` y `data/processed`.
- Integracion con web existente.
- Tests unitarios.

## 11. Riesgos y controles

| Riesgo | Control propuesto |
|---|---|
| Servicio ECC sin autorizaciones correctas | Usuario tecnico y roles definidos con Basis |
| Exposicion excesiva por Cloud Connector | Publicar solo paths requeridos |
| Filtros incompletos generan mucho volumen | Validar rango de fechas obligatorio |
| Cambios en estructura WSDL rompen Python | Versionar contrato y agregar tests |
| Errores no trazables | Registrar log cabecera/detalle en ECC |
| Datos sensibles expuestos | Revisar campos antes de publicar servicio |

## 12. Proximo paso inmediato

Definir formalmente los campos de salida:

```text
1. Campos de cliente.
2. Campos de factura/documento.
3. Filtros obligatorios.
4. Volumen esperado.
5. Usuario tecnico.
6. Frecuencia de consulta.
```

Con eso se puede comenzar la construccion en `SE11` y `SE37`.
