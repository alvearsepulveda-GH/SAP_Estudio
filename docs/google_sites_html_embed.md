# HTML5 para Google Sites

Fecha: 2026-05-24

## Archivo creado

```text
web/google_site_embed_resiliencia.html
```

Este archivo contiene un prototipo HTML5 para pegar en Google Sites usando:

```text
Insertar > Incorporar > Codigo
```

## Como conectarlo a tu Google Sheet

1. Abre tu Google Sheet:

```text
resiliencia_financiera_tesis_mafi
```

2. Copia el ID desde la URL.

Ejemplo:

```text
https://docs.google.com/spreadsheets/d/ESTE_ES_EL_ID/edit
```

3. Abre el archivo:

```text
web/google_site_embed_resiliencia.html
```

4. Busca esta linea:

```javascript
spreadsheetId: "PEGAR_ID_DE_TU_GOOGLE_SHEET",
```

5. Reemplazala por el ID real:

```javascript
spreadsheetId: "TU_ID_REAL",
```

## Requisito importante

Para que el HTML sea autonomo, lee directamente el Google Sheet ubicado en Drive. La hoja debe estar publicada o accesible para lectura.

Opcion recomendada para prototipo:

```text
Archivo > Compartir > Publicar en la web
```

Publicar la hoja:

```text
base_mensual
```

El HTML ya no usa boton de seleccion de archivo local. La fuente unica esperada es el Google Sheet en Drive.

## Como insertarlo en Google Sites

1. Entra a Google Sites.
2. Abre tu sitio.
3. Selecciona:

```text
Insertar > Incorporar
```

4. Selecciona:

```text
Codigo
```

5. Copia todo el contenido de:

```text
web/google_site_embed_resiliencia.html
```

6. Pegalo en Google Sites.
7. Presiona:

```text
Siguiente > Insertar
```

8. Ajusta el alto del bloque para que se vea completo.

## Que muestra el prototipo

- Clientes.
- Segmentos cliente-equipo.
- RAPV.
- DOS promedio.
- Grafico de RAPV por grupo de equipos.
- Matriz RAPV con grupos de productos en eje X y agrupaciones de clientes en eje Y.
- Tabla mensual con margen post-venta, GAV, RAPV, DOS y cobranza.

## Hojas esperadas

El HTML lee principalmente:

```text
base_mensual
```

Campos clave esperados:

```text
periodo
codigo_cliente_sap
nombre_cliente
id_celda
familia_producto
subfamilia_producto
estado_ciclo_vida
industria
margen_postventa
gav_asignado
ratio_absorcion
dos
cobranza_alineada
```

## Matriz principal

La matriz usa:

```text
Eje X: familia_producto
Eje Y: industria
Celda: RAPV y DOS promedio
```

Colores:

```text
Verde: RAPV >= 1 y DOS <= 65
Amarillo: zona de observacion
Rojo: bajo RAPV o cobranza lenta
```
