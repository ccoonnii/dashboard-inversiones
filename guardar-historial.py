
import json
from datetime import datetime, timezone
from pathlib import Path

ARCHIVO_COTIZACIONES = Path("cotizaciones.json")
ARCHIVO_HISTORIAL = Path("historial.json")

def main():
    if not ARCHIVO_COTIZACIONES.exists():
        raise FileNotFoundError("No se encontró cotizaciones.json")

    with ARCHIVO_COTIZACIONES.open("r", encoding="utf-8") as archivo:
        cotizaciones = json.load(archivo)

    if not isinstance(cotizaciones, dict):
        raise ValueError("cotizaciones.json debe contener un objeto JSON")

    fecha = datetime.now(timezone.utc).date().isoformat()
    registro = {
        "fecha": fecha,
        "cotizaciones": {}
    }

    for simbolo, datos in cotizaciones.items():
        if not isinstance(datos, dict):
            continue

        precio = datos.get("precio")
        if precio is None:
            precio = datos.get("price")

        if isinstance(precio, (int, float)) and precio > 0:
            registro["cotizaciones"][simbolo] = precio

    if not registro["cotizaciones"]:
        raise ValueError("No se encontraron precios válidos")

    if ARCHIVO_HISTORIAL.exists():
        with ARCHIVO_HISTORIAL.open("r", encoding="utf-8") as archivo:
            historial = json.load(archivo)
    else:
        historial = []

    if not isinstance(historial, list):
        raise ValueError("historial.json debe contener una lista JSON")

    # Si ya hay un registro de hoy, lo actualizamos en vez de duplicarlo.
    historial = [
        item for item in historial
        if item.get("fecha") != fecha
    ]
    historial.append(registro)
    historial.sort(key=lambda item: item.get("fecha", ""))

    with ARCHIVO_HISTORIAL.open("w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=2, ensure_ascii=False)
        archivo.write("\n")

    print(f"Historial actualizado: {fecha}")
    print(f"Activos registrados: {len(registro['cotizaciones'])}")

if __name__ == "__main__":
    main()

