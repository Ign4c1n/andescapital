# Andes Capital | Radar Bursátil

Versión visual completa de la app Andes Capital, diseñada para verse como una plataforma de análisis bursátil premium.

## Archivos incluidos

- `index.html`: app web estática.
- `styles.css`: diseño visual completo.
- `app.js`: interacción, gráfico, watchlist, señales y actualización.
- `streamlit_app.py`: versión lista para publicar en Streamlit Cloud.
- `assets/andes_capital_logo.png`: logo oficial usado en la interfaz.

## Publicar en Streamlit Cloud

1. Sube estos archivos a un repositorio de GitHub.
2. En Streamlit Cloud, crea una nueva app.
3. En "Main file path", escribe:

```bash
streamlit_app.py
```

4. Publica.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Nota importante

Esta versión prioriza diseño e interfaz. Los datos mostrados son de demostración para construir la experiencia visual.
El siguiente paso es conectar datos reales: Yahoo Finance, Stooq, Alpha Vantage, una API pagada o scraping controlado desde fuentes nacionales.
