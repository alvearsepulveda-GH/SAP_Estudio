# Conversacion del Proyecto SAP Estudio

Fecha: 2026-05-11

## Directorio del proyecto

```text
/Users/alejandroalvear/Documents/Alejandro/Desarrollo/Finanzas/MachineLearning/SAP_Estudio
```

## Objetivo general

El proyecto `SAP_Estudio` busca construir una solucion para recuperar informacion desde SAP, procesarla localmente y visualizarla en una pagina web.

El flujo deseado es:

```text
SAP
  -> extraccion de clientes y facturas/documentos enviados
  -> procesamiento local con Python
  -> archivos limpios en data/processed
  -> visualizacion web para consulta por cliente
```

## Estructura actual del proyecto

```text
SAP_Estudio/
├── src/sap_estudio/
│   ├── config.py
│   ├── sap_client.py
│   ├── extract.py
│   └── transform.py
├── web/
│   ├── app.py
│   ├── templates/index.html
│   └── static/styles.css
├── tests/
├── notebooks/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── reports/
├── pyproject.toml
└── README.md
```

## Git y GitHub

Se confirmo que el proyecto debe ser un repositorio distinto a la tarea del magister.

Repositorio local:

```text
/Users/alejandroalvear/Documents/Alejandro/Desarrollo/Finanzas/MachineLearning/SAP_Estudio
```

Repositorio remoto correcto:

```text
https://github.com/alvearsepulveda-GH/SAP_Estudio.git
```

Se realizo el primer commit local:

```text
686c41d Inicializa proyecto SAP Estudio
```

Y se subio la rama `main` al remoto:

```bash
git push -u origin main
```

Despues de esa configuracion, para subir nuevos cambios basta con:

```bash
git push
```

## Alternativas conversadas para conectar con SAP

### SAP GUI Scripting con Visual Basic

Se converso la posibilidad de usar SAP GUI Scripting:

```text
SAP GUI
  -> grabacion SAP Script
  -> archivo .vbs
  -> ejecucion automatica
  -> exportacion a Excel/CSV
  -> lectura con Python
```

Ventajas:

- Puede servir si ya existe una transaccion manual.
- Es rapido para prototipos.

Limitaciones:

- Depende de SAP GUI.
- Normalmente requiere Windows.
- Es fragil ante cambios de pantalla o tiempos de carga.
- No es la opcion mas robusta para produccion.

### WSDL/SOAP con SAP BTP

Luego se propuso un enfoque mas profesional usando un servicio WSDL/SOAP expuesto desde SAP ECC y consumido a traves de SAP BTP.

Flujo objetivo:

```text
Programa Python / App
  -> SAP BTP
  -> Destination / Cloud Connector
  -> Servicio SOAP WSDL en SAP ECC
  -> Datos de clientes y facturas
  -> Transformacion
  -> Visualizacion web
```

Ventajas:

- No depende de pantallas.
- Es mas estable y automatizable.
- Permite manejo mas limpio de errores.
- Es mas adecuado para integraciones reales.

## Pasos propuestos en SAP ECC

### 1. Crear estructuras en SE11

Para este caso no se recomienda crear tablas fisicas Z si solo se van a leer datos existentes de SAP. Lo recomendable es crear estructuras y tipos tabla.

Estructura de cliente:

```text
ZST_SAP_ESTUDIO_CLIENTE
```

Campos sugeridos:

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

Tipo tabla de clientes:

```text
ZTT_SAP_ESTUDIO_CLIENTE
```

Line type:

```text
ZST_SAP_ESTUDIO_CLIENTE
```

Estructura de factura:

```text
ZST_SAP_ESTUDIO_FACTURA
```

Campos sugeridos:

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

Tipo tabla de facturas:

```text
ZTT_SAP_ESTUDIO_FACTURA
```

Line type:

```text
ZST_SAP_ESTUDIO_FACTURA
```

### 2. Columna "Clase tipificacion" en SE11

En una estructura de SE11, la columna `Clase tipificacion` normalmente debe quedar como:

```text
TYPE
```

Ejemplo:

```text
Componente   Clase tipificacion   Tipo componente
KUNNR        TYPE                  KUNNR
NAME1        TYPE                  NAME1_GP
STCD1        TYPE                  STCD1
```

Si SAP no reconoce algun tipo o se quiere copiar directamente desde una tabla estandar, tambien se puede usar:

```text
LIKE
```

Ejemplo:

```text
Componente   Clase tipificacion   Tipo componente
KUNNR        LIKE                  KNA1-KUNNR
NAME1        LIKE                  KNA1-NAME1
STCD1        LIKE                  KNA1-STCD1
ORT01        LIKE                  KNA1-ORT01
LAND1        LIKE                  KNA1-LAND1
```

Recomendacion practica inicial:

```text
Usar LIKE con campos de tablas estandar cuando se quiera evitar errores con nombres de elementos de datos.
```

### 3. Crear Function Module en SE37

Nombre sugerido:

```text
ZFM_SAP_ESTUDIO_DATOS
```

Debe ser marcado como:

```text
Remote-Enabled Module
```

Parametros sugeridos:

```text
IMPORTING
  IV_FECHA_DESDE
  IV_FECHA_HASTA
  IV_CLIENTE

EXPORTING / TABLES
  ET_CLIENTES
  ET_FACTURAS
```

El Function Module consultaria tablas SAP como:

```text
KNA1   Maestro general de clientes
KNVV   Datos comerciales del cliente
VBRK   Cabecera de facturas
VBRP   Posiciones de facturas
```

### 4. Exponer como Web Service SOAP

Despues de probar el Function Module en `SE37`, se debe exponer como servicio SOAP:

```text
Function Module
  -> Web Service / Service Definition
  -> SOAMANAGER
  -> Binding / Endpoint
  -> WSDL
```

## Pasos propuestos en SAP BTP

1. Configurar SAP Cloud Connector en la red donde esta ECC.
2. Conectar Cloud Connector al subaccount de SAP BTP.
3. Crear mapping hacia el sistema ECC.
4. Exponer solo los paths necesarios, por ejemplo:

```text
/sap/bc/srt/
```

5. Crear una Destination en SAP BTP:

```text
Type: HTTP
Proxy Type: OnPremise
Authentication: BasicAuthentication o el mecanismo definido por Basis
URL: host virtual del Cloud Connector
```

6. El programa consumidor usaria esa Destination para llamar al servicio SOAP.

## Programa consumidor en Python

Se propuso usar `zeep` para consumir el WSDL desde Python.

Ejemplo conceptual:

```python
from zeep import Client

WSDL_URL = "URL_DEL_WSDL"

client = Client(WSDL_URL)

response = client.service.ZFM_SAP_ESTUDIO_DATOS(
    IV_FECHA_DESDE="2026-05-01",
    IV_FECHA_HASTA="2026-05-31",
    IV_CLIENTE=""
)
```

Luego el programa debe:

1. Convertir la respuesta SOAP/XML a `pandas.DataFrame`.
2. Guardar datos originales en `data/raw/`.
3. Transformar y validar datos.
4. Guardar archivos limpios en `data/processed/`.
5. Mostrar la informacion en la aplicacion web.

## Proximos pasos

1. Definir los campos exactos de cliente.
2. Definir los campos exactos de factura/documento.
3. Crear estructuras y tipos tabla en `SE11`.
4. Crear y probar el Function Module en `SE37`.
5. Exponer el servicio en `SOAMANAGER`.
6. Obtener el WSDL.
7. Configurar Cloud Connector y Destination en SAP BTP.
8. Implementar el cliente SOAP en Python dentro del proyecto.
