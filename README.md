# Wallapop Route Helper

Este repositorio contiene un pequeño script de ejemplo escrito en Python.
El script obtiene una ruta utilizando la API de Google Maps y realiza
consultas a la API de Wallapop para listar los objetos en venta cercanos a
dicha ruta.

## Requisitos

- Python 3.11+
- Una clave de la API de Google Maps (variable de entorno `GOOGLE_MAPS_API_KEY`)

Para instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

```bash
export GOOGLE_MAPS_API_KEY=tu_clave
python wallapop_route.py "Madrid" "Barcelona"
```

El programa imprimirá en consola los artículos encontrados a lo largo de
la ruta. Ten en cuenta que el endpoint público de Wallapop puede cambiar
o requerir autenticación adicional.
