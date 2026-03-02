import argparse
from pathlib import Path
import pandas as pd
from src.clean import limpiar
from src.analysis import tabla_resumen_region
from src.zenodo import descargar_archivo_zenodo_por_doi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", type=str, default="data/raw/solicitudes_crudas.csv")
    parser.add_argument("--salida", type=str, default="data/processed/solicitudes_limpias.csv")
    parser.add_argument("--tabla", type=str, default="results/tables/tabla_resumen_region.csv")
    parser.add_argument("--doi", type=str, default="10.5281/zenodo.18829497")
    parser.add_argument("--archivo_zenodo", type=str, default="solicitudes_crudas.csv")
    args = parser.parse_args()

    raiz = Path(__file__).resolve().parents[1]

    ruta_entrada = Path(args.entrada)
    if not ruta_entrada.is_absolute():
        ruta_entrada = raiz / ruta_entrada

    ruta_salida = Path(args.salida)
    if not ruta_salida.is_absolute():
        ruta_salida = raiz / ruta_salida
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    ruta_tabla = Path(args.tabla)
    if not ruta_tabla.is_absolute():
        ruta_tabla = raiz / ruta_tabla
    ruta_tabla.parent.mkdir(parents=True, exist_ok=True)

    descargar_archivo_zenodo_por_doi(
        doi=args.doi,
        nombre_archivo=args.archivo_zenodo,
        ruta_destino=ruta_entrada,
    )

    crudo = pd.read_csv(ruta_entrada, encoding="utf-8")
    limpio = limpiar(crudo)
    limpio.to_csv(ruta_salida, index=False, encoding="utf-8")

    resumen = tabla_resumen_region(limpio)
    resumen.to_csv(ruta_tabla, encoding="utf-8")

    print(str(ruta_salida))
    print(str(ruta_tabla))


if __name__ == "__main__":
    main()
