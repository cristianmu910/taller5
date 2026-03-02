from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.request import urlopen, urlretrieve

def _record_id_desde_doi(doi: str) -> str:
    m = re.search(r"zenodo\.(\d+)", doi)
    if not m:
        raise ValueError(f"DOI inválido o no es de Zenodo: {doi}")
    return m.group(1)

def descargar_archivo_zenodo_por_doi(
    doi: str,
    nombre_archivo: str,
    ruta_destino: str | Path,
) -> Path:
    record_id = _record_id_desde_doi(doi)
    api_url = f"https://zenodo.org/api/records/{record_id}"

    with urlopen(api_url) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    archivos = payload.get("files", [])
    if not archivos:
        raise RuntimeError("El registro no trae archivos en la API de Zenodo.")

    match = None
    for f in archivos:
        if f.get("key") == nombre_archivo:
            match = f
            break

    if match is None:
        disponibles = [f.get("key") for f in archivos]
        raise FileNotFoundError(
            f"No encontré '{nombre_archivo}' en Zenodo. Disponibles: {disponibles}"
        )

    download_url = match["links"]["self"]  # link directo al archivo
    ruta_destino = Path(ruta_destino)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    urlretrieve(download_url, ruta_destino)
    return ruta_destino