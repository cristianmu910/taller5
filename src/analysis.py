import pandas as pd
import matplotlib.pyplot as plt


def tabla_resumen_region(df: pd.DataFrame) -> pd.DataFrame:
    resumen = (
        df.groupby("region")
        .agg(
            solicitudes=("id_cliente", "size"),
            aprobacion=("aprobado", "mean"),
            mora=("mora_90d", "mean"),
            monto_prom=("monto_solicitado", "mean")
        )
        .sort_values("solicitudes", ascending=False)
    )
    return resumen


def mora_por_quintil(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["quintil_ingreso"] = pd.qcut(temp["ingreso_mensual"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
    mora_quintil = temp.groupby("quintil_ingreso")["mora_90d"].mean().reset_index()
    return mora_quintil


def guardar_figura_mora_quintil(mora_quintil: pd.DataFrame, ruta_png):
    plt.figure()
    plt.plot(mora_quintil["quintil_ingreso"].astype(str), mora_quintil["mora_90d"])
    plt.title("Tasa de mora por quintil de ingreso (mejorada)")
    plt.xlabel("Quintil de ingreso")
    plt.ylabel("Tasa de mora (%)")
    plt.tight_layout()
    plt.savefig(ruta_png, dpi=160)
    plt.close()
