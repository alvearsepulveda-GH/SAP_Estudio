# Tesis MAFI USACH - Resiliencia Financiera

Fecha: 2026-05-24

## Tema

Modelamiento de la resiliencia financiera mediante la optimizacion del mix de negocios y la cobertura de post-venta en la industria de maquinaria pesada en Chile.

## Idea central

La tesis cruza dos jerarquias:

```text
Jerarquia de clientes
  x
Jerarquia de grupos de equipos
```

Cada interseccion genera una celda analitica. En cada celda vive el indicador principal:

```text
RAPV = Margen post-venta / GAV asignado
```

Donde:

```text
Margen post-venta = margen repuestos + margen servicios + margen arriendos
GAV = gasto de administracion y ventas asignado al periodo/celda
```

Tambien se incorpora:

```text
DOS = days of standing / dias de cobranza
```

Esto permite identificar si una linea de negocio aporta al ratio de absorcion y si ademas esta alineada con la recuperacion de caja.

## Alcance inicial

```text
Pais: Chile
Periodo simulado: 2020-01 a 2025-12
Meses: 72
Clientes simulados: 12
Productos/equipos simulados: 6
Celdas cliente-equipo: 36
Registros mensuales: 2.592
```

## Grupos de equipos

```text
Motores
Generadores
Soporte electrico
```

Subfamilias incluidas:

```text
Motores estaticos
Motores maritimos
Generadores diesel
Generadores respaldo
UPS
Tableros electricos
```

## Estado comercial y ciclo de vida

Cada celda distingue si el equipo corresponde a:

```text
Equipo comercializado hoy
Equipo no comercializado / legado
```

Y su estado de ciclo de vida:

```text
Vendido actual
En servicio
Proximo a renovacion
Fin de vida util
```

Esto permite plantear una oportunidad de reinversion cuando existen equipos legacy, equipos cercanos al fin de vida util o lineas con buen margen pero baja recuperacion de caja.

## Archivo Excel generado

Ruta local en el proyecto:

```text
data/processed/resiliencia_financiera_tesis_mafi.xlsx
```

Ruta OneDrive:

```text
/Users/alejandroalvear/Library/CloudStorage/OneDrive-Finning/SAP_Estudio/resiliencia_financiera_tesis_mafi.xlsx
```

Google Sheet:

```text
https://docs.google.com/spreadsheets/d/1S9WrNiQav7JQiB4EG0gT6COGqenvmT4SJbrf7EM97gk
```

## Hojas del libro

```text
Dashboard
Matriz_RAPV
base_mensual
clientes
productos_equipos
celdas
gav_mensual
supuestos
diccionario
```

## Uso para Google Sites

Para el prototipo:

1. Crear sitio en Google Sites.
2. Titulo: `Resiliencia financiera Chile`.
3. Insertar el Google Sheet:

```text
MAFI USACH - Resiliencia financiera maquinaria pesada Chile
```

4. Mostrar la hoja:

```text
Dashboard
```

5. Agregar secciones de explicacion:

```text
Planteamiento del problema
Variables
Matriz cliente x equipo
RAPV
DOS / cobranza
Oportunidades de reinversion
```

## Generador

La simulacion se genera con:

```bash
python3 scripts/generate_resilience_simulation.py
```

El script es deterministico y usa semilla fija para que los datos puedan regenerarse con los mismos supuestos.
