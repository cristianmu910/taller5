import argparse
from pathlib import Path
from src.simulate import simular_solicitudes, ensuciar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filas", type=int, default=2000)
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--semilla_sucio", type=int, default=7)
    parser.add_argument("--salida", type=str, default="data/raw/solicitudes_crudas.csv")
    args = parser.parse_args()

    raiz = Path(__file__).resolve().parents[1]

    ruta_salida = Path(args.salida)
    if not ruta_salida.is_absolute():
        ruta_salida = raiz / ruta_salida
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    base = simular_solicitudes(args.filas, args.semilla)
    sucio = ensuciar(base, args.semilla_sucio)

    sucio.to_csv(ruta_salida, index=False, encoding="utf-8")
    print(str(ruta_salida))


if __name__ == "__main__":
    main()
