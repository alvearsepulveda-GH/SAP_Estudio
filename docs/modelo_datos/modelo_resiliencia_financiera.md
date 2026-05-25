# Modelo de Datos - Resiliencia Financiera

Fecha: 2026-05-22

## Objetivo

Construir una base de datos mensual de los ultimos 5 anos para medir resiliencia financiera cruzando:

- Jerarquia de clientes.
- Jerarquia de productos/equipos.
- Codigos SAP de cliente.
- Codigos SAP de material.
- Facturacion mensual.
- Costo de administracion y ventas.
- Ratio de absorcion.

Alcance inicial:

```text
Pais: Chile
Sociedad SAP inicial: CL01
```

## Concepto central

La celda analitica cruza un cliente con un producto/equipo:

```text
Cliente / Jerarquia cliente
  x
Producto o equipo / Jerarquia producto
  =
Celda de resiliencia financiera
```

En cada celda se calcula:

```text
Ratio absorcion =
(Ventas repuestos + Ventas servicios + Ventas arriendos)
/ Costo administracion y ventas
```

Si se quiere expresar como porcentaje:

```text
Ratio absorcion % =
((Ventas repuestos + Ventas servicios + Ventas arriendos)
/ Costo administracion y ventas) * 100
```

## Tablas maestras

### 1. Jerarquia de clientes

Archivo:

```text
data/templates/clientes_jerarquia_template.csv
```

Campos:

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

Jerarquia sugerida para Chile:

```text
Chile
  -> Sociedad SAP
    -> Industria
      -> Grupo economico
        -> Cliente
          -> Faena / operacion
```

### 2. Jerarquia de productos/equipos

Archivo:

```text
data/templates/productos_equipos_jerarquia_template.csv
```

Campos:

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

Jerarquia sugerida:

```text
Familia producto
  -> Subfamilia producto
    -> Linea negocio
      -> Tipo equipo
        -> Modelo
          -> Codigo material SAP
```

Familias iniciales:

```text
Motores
Generadores
Equipos de soporte electrico
```

Subfamilias iniciales:

```text
Motores estaticos
Motores maritimos
Generadores diesel
UPS
Tableros electricos
Banco de baterias
```

Estados de ciclo de vida sugeridos:

```text
Vendido actual
En servicio
Vida util media
Proximo a renovacion
Fin de vida util
Fuera de servicio
```

## Tabla puente: celdas cliente-producto

Archivo:

```text
data/templates/celdas_cliente_producto_template.csv
```

Esta tabla define que codigos de cliente y material caen en cada celda analitica.

Campos:

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

Uso:

```text
1. Poblar clientes desde SAP.
2. Poblar materiales/equipos desde SAP.
3. Clasificar cada material en la jerarquia de productos.
4. Asociar cliente + material en una celda.
5. Usar id_celda para traer facturacion mensual y calcular ratio.
```

## Tabla de hechos mensual

Archivo:

```text
data/templates/base_mensual_resiliencia_template.csv
```

Campos:

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

Granularidad:

```text
1 fila por periodo mensual + cliente + material/equipo/celda
```

Periodo recomendado:

```text
Ultimos 5 anos, en formato YYYY-MM.
```

Ejemplo:

```text
2021-01
2021-02
...
2026-05
```

## Reglas de calculo

### Ventas absorbentes

```text
ventas_absorbentes =
ventas_repuestos + ventas_servicios + ventas_arriendos
```

### Ratio de absorcion

```text
ratio_absorcion =
ventas_absorbentes / costo_administracion_ventas
```

Si el costo de administracion y ventas es cero:

```text
ratio_absorcion = 0
```

### Lectura del indicador

```text
ratio_absorcion > 1.0  La celda absorbe mas que su costo asignado.
ratio_absorcion = 1.0  Punto de equilibrio.
ratio_absorcion < 1.0  La celda no absorbe completamente su costo asignado.
```

## Flujo de carga propuesto

```text
SAP
  -> exportar clientes
  -> exportar materiales/equipos
  -> exportar facturacion mensual
  -> exportar costos administracion y ventas
  -> poblar tablas maestras
  -> poblar celdas cliente-producto
  -> generar base mensual de 5 anos
  -> calcular ratio de absorcion
  -> publicar en Excel / OneDrive / SharePoint
```

En la primera version, los filtros de pais deben retornar solo:

```text
Chile
```

## Archivo Excel para consulta web

La aplicacion web inicial lee el archivo:

```text
data/processed/resiliencia_financiera.xlsx
```

Tambien se puede apuntar a un Excel sincronizado en OneDrive usando la variable de entorno:

```text
SAP_ESTUDIO_EXCEL_PATH=/ruta/al/archivo/resiliencia_financiera.xlsx
```

Para este proyecto, la ruta OneDrive definida es:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio/resiliencia_financiera.xlsx
```

El libro debe tener estas hojas:

```text
clientes
productos_equipos
celdas
base_mensual
```

## Salidas esperadas

### Matriz de resiliencia

Filas:

```text
Pais -> Sociedad -> Industria -> Grupo economico -> Cliente -> Faena
```

Columnas:

```text
Familia producto -> Subfamilia -> Tipo equipo -> Estado ciclo de vida
```

Celda:

```text
Ratio de absorcion mensual
```

### Indicadores derivados

```text
Ratio promedio 12 meses
Ratio promedio 5 anos
Tendencia mensual
Clientes bajo punto de equilibrio
Familias de producto mas resilientes
Clientes con alto potencial de renovacion
Base instalada cercana a fin de vida util
```

## Proximo paso

Completar las tablas maestras con codigos reales SAP:

```text
1. Codigos de cliente.
2. Nombre de cliente.
3. Pais y sociedad.
4. Codigos de material.
5. Familia y subfamilia de producto.
6. Estado del ciclo de vida.
```

Luego se puede construir el proceso Python para generar automaticamente la base mensual.
