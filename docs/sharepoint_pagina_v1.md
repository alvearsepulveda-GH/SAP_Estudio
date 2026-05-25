# Pagina SharePoint V1 - Resiliencia Financiera Chile

Fecha: 2026-05-24

## Objetivo

Crear una pagina SharePoint version 1 para publicar el Excel de resiliencia financiera generado desde SAP mediante VBScript.

## Archivo a insertar

El archivo queda en OneDrive corporativo:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio/resiliencia_financiera.xlsx
```

Nombre del archivo:

```text
resiliencia_financiera.xlsx
```

Hoja principal para mostrar:

```text
Dashboard
```

## Titulo de la pagina

```text
Resiliencia financiera Chile
```

## Secciones sugeridas

### 1. Resumen ejecutivo

Web part:

```text
Texto
```

Contenido:

```text
Esta pagina consolida una primera version del modelo de resiliencia financiera para Chile, cruzando clientes, productos/equipos, facturacion mensual y costos de administracion y ventas.

El indicador principal es el ratio de absorcion:

(Ventas de repuestos + ventas de servicios + ventas de arriendos) / costo de administracion y ventas.
```

### 2. Dashboard Excel

Web part:

```text
Archivo y multimedia
```

o:

```text
File viewer
```

Archivo:

```text
SAP_Estudio/resiliencia_financiera.xlsx
```

Hoja recomendada:

```text
Dashboard
```

### 3. Documentacion del proceso

Web part:

```text
Texto
```

Contenido:

```text
Los datos son recuperados desde SAP mediante un VBScript, guardados en un Excel dentro de OneDrive corporativo y publicados en esta pagina de SharePoint.

La version 1 usa Excel como fuente principal. En una version posterior, el modelo puede evolucionar a SharePoint List, Power BI o una aplicacion web integrada.
```

### 4. Enlaces rapidos

Web part:

```text
Vinculos rapidos
```

Enlaces sugeridos:

```text
Excel resiliencia_financiera.xlsx
Carpeta OneDrive SAP_Estudio
Documentacion del modelo
Repositorio SAP_Estudio
```

## Pasos para construir la pagina

1. Entrar al sitio SharePoint corporativo.
2. Seleccionar:

```text
Nuevo > Pagina
```

3. Elegir pagina en blanco.
4. Usar el titulo:

```text
Resiliencia financiera Chile
```

5. Agregar una seccion de texto con el resumen ejecutivo.
6. Agregar el web part:

```text
Archivo y multimedia
```

7. Seleccionar el archivo:

```text
resiliencia_financiera.xlsx
```

8. Configurar la vista para mostrar la hoja:

```text
Dashboard
```

9. Agregar una seccion de documentacion del proceso.
10. Agregar vinculos rapidos.
11. Publicar la pagina.

## Nota

No tengo acceso autenticado al SharePoint corporativo desde este entorno, por lo que la publicacion final debe hacerse desde tu sesion corporativa. El contenido, el archivo Excel y la estructura de pagina ya quedan preparados para montar la version 1.
