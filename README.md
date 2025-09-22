# Dashboard Interactivo de Gastos 💰📊

Proyecto avanzado en Python que permite gestionar y analizar tus gastos de manera profesional, con visualizaciones interactivas y filtros personalizables.

---

## Contenido

- `gestor_gastos.py` → Script de consola para agregar, resumir y graficar gastos en un archivo CSV.
- `app.py` → Dashboard interactivo con Streamlit que permite:
  - Subir un CSV de gastos
  - Filtrar por fechas y categorías
  - Visualizar gráficos interactivos (línea temporal, barras, torta)
  - Descargar datos filtrados en CSV

---

## Librerías necesarias

- `pandas`
- `matplotlib`
- `plotly`
- `streamlit`

Todas se pueden instalar con:

- pip install -r requirements.txt

## Uso

1️⃣ Gestor de gastos por consola
python gestor_gastos.py

Opciones:
Agregar gasto (puedes elegir la fecha o dejar la actual)
Ver resumen por categoría
Graficar gastos por categoría
Salir
Se genera automáticamente el archivo gastos.csv si no existe.

2️⃣ Dashboard Interactivo con Streamlit
streamlit run app.py

Se abre una página web local donde podés:
Subir tu CSV de gastos
Activar un dataset de ejemplo
Filtrar por fechas y categorías
Ver gráficos interactivos
Descargar CSV filtrado
Formato CSV esperado:

date	category	description	amount
2024-01-05	Comida	Almuerzo	1200
2024-01-06	Transporte	Subte	350

## Notas

- Este proyecto es educativo, pero simula un flujo profesional de análisis financiero.

## Autor

- Juan Manuel Sala García