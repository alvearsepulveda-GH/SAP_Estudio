# Flujo SAP GUI Scripting, OneDrive y SharePoint

Fecha: 2026-05-24

## Objetivo

Recuperar datos desde SAP usando un `VBScript`, guardar el resultado en un Excel dentro de OneDrive corporativo y consultar esa informacion desde la web del proyecto `SAP_Estudio`.

## Ruta OneDrive definida

El Excel principal debe quedar en:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio/resiliencia_financiera.xlsx
```

La carpeta creada es:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio
```

## Flujo operativo

```text
SAP GUI
  -> VBScript ejecuta transaccion o reporte
  -> exporta datos a Excel
  -> guarda o reemplaza resiliencia_financiera.xlsx en OneDrive
  -> OneDrive sincroniza el archivo
  -> web SAP_Estudio lee el Excel
  -> SharePoint publica o enlaza la informacion
```

## Configuracion de la web

La aplicacion lee la ruta definida por la variable:

```text
SAP_ESTUDIO_EXCEL_PATH
```

Ejemplo:

```text
SAP_ESTUDIO_EXCEL_PATH=/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio/resiliencia_financiera.xlsx
```

Si la variable no existe, usa el archivo local del proyecto:

```text
data/processed/resiliencia_financiera.xlsx
```

## Estructura esperada del Excel

El libro debe contener estas hojas:

```text
clientes
productos_equipos
celdas
base_mensual
```

### Hoja `clientes`

```text
id_cliente
codigo_cliente_sap
nombre_cliente
pais
sociedad_sap
industria
grupo_economico
segmento
faena_operacion
region
ciudad
estado_cliente
fecha_inicio_relacion
```

### Hoja `productos_equipos`

```text
id_producto_equipo
codigo_material_sap
descripcion_material
familia_producto
subfamilia_producto
linea_negocio
tipo_equipo
modelo
equipo_nuevo_o_base_instalada
estado_ciclo_vida
vida_util_esperada_meses
```

### Hoja `celdas`

```text
id_celda
id_cliente
id_producto_equipo
codigo_cliente_sap
codigo_material_sap
pais
sociedad_sap
familia_producto
subfamilia_producto
estado_ciclo_vida
activo_desde
activo_hasta
```

### Hoja `base_mensual`

```text
periodo
id_celda
codigo_cliente_sap
codigo_material_sap
pais
sociedad_sap
ventas_repuestos
ventas_servicios
ventas_arriendos
ventas_equipos_nuevos
costo_administracion_ventas
ratio_absorcion
moneda
```

## Recomendacion para el VBScript

El `VBScript` debe guardar siempre el archivo con el mismo nombre:

```text
resiliencia_financiera.xlsx
```

Y en la misma carpeta OneDrive:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio
```

En Windows, la ruta equivalente probablemente sera algo similar a:

```text
C:\Users\<usuario>\OneDrive - Finning\SAP_Estudio\resiliencia_financiera.xlsx
```

Cuando definamos el equipo donde correra el `VBScript`, se debe ajustar esa ruta al path real de OneDrive en Windows.

## Regla importante

El archivo que exporte SAP debe respetar los nombres de hojas y columnas esperados por la web. Si SAP exporta una hoja plana diferente, se necesitara un paso intermedio de transformacion para convertirla al formato `SAP_Estudio`.
