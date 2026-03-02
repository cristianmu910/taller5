import argparse
from pathlib import Path
import pandas as pd
from src.analysis import mora_por_quintil, guardar_figura_mora_quintil


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", type=str, default="data/processed/solicitudes_limpias.csv")
    parser.add_argument("--figura", type=str, default="results/figures/figura_mora_quintil.png")
    args = parser.parse_args()

    raiz = Path(__file__).resolve().parents[1]

    ruta_entrada = Path(args.entrada)
    if not ruta_entrada.is_absolute():
        ruta_entrada = raiz / ruta_entrada

    ruta_figura = Path(args.figura)
    if not ruta_figura.is_absolute():
        ruta_figura = raiz / ruta_figura
    ruta_figura.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(ruta_entrada, parse_dates=["fecha_solicitud"], encoding="utf-8")
    mora_q = mora_por_quintil(df)

    guardar_figura_mora_quintil(mora_q, ruta_figura)
    print(str(ruta_figura))


if __name__ == "__main__":
    main()
