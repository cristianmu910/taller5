import numpy as np
import pandas as pd


def simular_solicitudes(n_filas: int, semilla: int) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)

    regiones = ["Bogota", "Antioquia", "Valle", "Santander", "Costa"]
    sexos = ["M", "F"]
    plazos = [12, 24, 36, 48, 60]

    tabla = pd.DataFrame({
        "id_cliente": rng.integers(100000, 999999, size=n_filas),
        "fecha_solicitud": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, size=n_filas), unit="D"),
        "region": rng.choice(regiones, size=n_filas, p=[0.35, 0.2, 0.15, 0.15, 0.15]),
        "sexo": rng.choice(sexos, size=n_filas, p=[0.55, 0.45]),
        "plazo_meses": rng.choice(plazos, size=n_filas, p=[0.1, 0.2, 0.25, 0.25, 0.2]),
    })

    ingreso = rng.lognormal(mean=np.log(3_000_000), sigma=0.45, size=n_filas)
    ingreso = np.clip(ingreso, 900_000, 25_000_000)

    tasa_ea = rng.normal(loc=0.199, scale=0.03, size=n_filas)
    tasa_ea = np.clip(tasa_ea, 0.12, 0.28)

    monto = ingreso * rng.uniform(0.6, 2.2, size=n_filas) + (tabla["plazo_meses"].values * 60_000)
    monto = np.clip(monto, 500_000, 60_000_000)

    tabla["ingreso_mensual"] = ingreso.round(0).astype(int)
    tabla["tasa_ea"] = tasa_ea.round(4)
    tabla["monto_solicitado"] = monto.round(0).astype(int)

    puntaje = (
        0.6 * (tabla["ingreso_mensual"] / tabla["ingreso_mensual"].max())
        - 0.35 * (tabla["monto_solicitado"] / tabla["monto_solicitado"].max())
        - 0.15 * (tabla["tasa_ea"] / tabla["tasa_ea"].max())
        - 0.05 * (tabla["plazo_meses"] / 60)
        + rng.normal(0, 0.05, size=n_filas)
    )

    tabla["aprobado"] = (puntaje > 0.12).astype(int)

    prob_mora = (
        0.25
        + 0.35 * (tabla["tasa_ea"] - tabla["tasa_ea"].min()) / (tabla["tasa_ea"].max() - tabla["tasa_ea"].min())
        + 0.25 * (1 - (tabla["ingreso_mensual"] / tabla["ingreso_mensual"].max()))
        - 0.25 * tabla["aprobado"]
    )
    prob_mora = np.clip(prob_mora, 0.02, 0.75)
    tabla["mora_90d"] = (rng.random(n_filas) < prob_mora).astype(int)

    return tabla


def ensuciar(tabla: pd.DataFrame, semilla: int) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    sucio = tabla.copy()

    idx_dup = rng.choice(sucio.index, size=max(1, int(0.015 * len(sucio))), replace=False)
    sucio = pd.concat([sucio, sucio.loc[idx_dup]], ignore_index=True)

    idx_nulo_ing = rng.choice(sucio.index, size=int(0.04 * len(sucio)), replace=False)
    sucio.loc[idx_nulo_ing, "ingreso_mensual"] = np.nan

    idx_nulo_reg = rng.choice(sucio.index, size=int(0.02 * len(sucio)), replace=False)
    sucio.loc[idx_nulo_reg, "region"] = None

    idx_ing_neg = rng.choice(sucio.index, size=int(0.01 * len(sucio)), replace=False)
    sucio.loc[idx_ing_neg, "ingreso_mensual"] = -rng.integers(100_000, 2_000_000, size=len(idx_ing_neg))

    idx_monto_raro = rng.choice(sucio.index, size=int(0.01 * len(sucio)), replace=False)
    sucio.loc[idx_monto_raro, "monto_solicitado"] = rng.integers(80_000_000, 200_000_000, size=len(idx_monto_raro))

    idx_fmt_ing = rng.choice(sucio.index, size=int(0.06 * len(sucio)), replace=False)
    for i in idx_fmt_ing:
        valor = sucio.loc[i, "ingreso_mensual"]
        if pd.isna(valor):
            continue
        estilo = rng.choice(["$1.234.567", "1,234,567", "1.234.567", "1,2e6"])
        if estilo == "$1.234.567":
            sucio.loc[i, "ingreso_mensual"] = f"${int(valor):,}".replace(",", ".")
        elif estilo == "1,234,567":
            sucio.loc[i, "ingreso_mensual"] = f"{int(valor):,}"
        elif estilo == "1.234.567":
            sucio.loc[i, "ingreso_mensual"] = f"{int(valor):,}".replace(",", ".")
        else:
            sucio.loc[i, "ingreso_mensual"] = "1,2e6"

    idx_fmt_monto = rng.choice(sucio.index, size=int(0.05 * len(sucio)), replace=False)
    for i in idx_fmt_monto:
        valor = sucio.loc[i, "monto_solicitado"]
        if pd.isna(valor):
            continue
        estilo = rng.choice(["$12.345.678", "12,345,678", "12.345.678"])
        if estilo == "$12.345.678":
            sucio.loc[i, "monto_solicitado"] = f"${int(valor):,}".replace(",", ".")
        elif estilo == "12,345,678":
            sucio.loc[i, "monto_solicitado"] = f"{int(valor):,}"
        else:
            sucio.loc[i, "monto_solicitado"] = f"{int(valor):,}".replace(",", ".")

    idx_reg = rng.choice(sucio.index, size=int(0.07 * len(sucio)), replace=False)
    for i in idx_reg:
        r = sucio.loc[i, "region"]
        if r is None or pd.isna(r):
            continue
        r = str(r)
        sucio.loc[i, "region"] = rng.choice([r.lower(), " " + r + "  ", r.replace("Bogota", "Bogotá"), "costaa" if r == "Costa" else r])

    idx_sexo = rng.choice(sucio.index, size=int(0.05 * len(sucio)), replace=False)
    for i in idx_sexo:
        s = str(sucio.loc[i, "sexo"])
        sucio.loc[i, "sexo"] = rng.choice([s.lower(), "Masculino" if s == "M" else "Femenino", " " + s + " "])

    return sucio
