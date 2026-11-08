# FreeDNS Afraid.org Domain Scraper

Este proyecto extrae todos los dominios disponibles de [freedns.afraid.org](https://freedns.afraid.org/) que pueden utilizarse para el registro gratuito de subdominios.

<div align="center">
    <h3>Ver los dominios disponibles:</h3>
    <a href="domains-alphabetical.md">Dominios Alfabéticos</a> | <a href="domains-length.md">Dominios por Longitud</a>
</div>

## Características

- Extrae los ~25,000 dominios públicos del registro
- Maneja la paginación
- Extrae el dominio, estado, propietario, antigüedad y hosts en uso
- Genera tablas en markdown: ordenadas alfabéticamente y por longitud
- Automatizado mediante GitHub Actions cada 12 horas

## Requisitos

- Python 3.9+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el scraper:
```bash
python scraper.py
```

Ejecuta el scraper con una cantidad `n` de páginas (cada página contiene aproximadamente 100 dominios):
```bash
python scraper.py -p 10
```

El script hará lo siguiente:
1. Extraerá todas las páginas del registro de dominios
2. Extraerá la información del dominio desde las tablas HTML
3. Guardará los resultados en `domains-alphabetical.md` y `domains-length.md`

## Automatización (GitHub Actions)

El proyecto ejecuta una GitHub Action automáticamente cada 24 horas para actualizar la lista de dominios.

Para configurarlo:
1. Sube este código a un repositorio de GitHub
2. Asegúrate de que GitHub Actions esté habilitado
3. El flujo de trabajo se ejecutará según el horario programado y realizará el commit de las actualizaciones en los archivos markdown

También puedes activarlo manualmente a través de la pestaña Actions.

## Salida

- `domains-alphabetical.md`: Dominios ordenados alfabéticamente
- `domains-length.md`: Dominios ordenados por longitud (del más corto al más largo), y luego alfabéticamente (ab.cd, luego ac.cd)
