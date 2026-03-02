import re
import numpy as np
import pandas as pd


def a_numero(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.integer, np.floating)):
        return float(x)

    s = str(x).strip()

    if re.search(r"e6$", s, flags=re.IGNORECASE):
        s2 = s.lower().replace("e6", "")
        s2 = s2.replace("$", "").replace(".", "").replace(",", ".")
        s2 = re.sub(r"\s+", "", s2)
        try:
            return float(s2) * 1_000_000
        except ValueError:
            return np.nan

    s2 = s.replace("$", "").strip()

    if re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{3})+(?:,[0-9]+)?", s2):
        s2 = s2.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"[0-9]{1,3}(?:,[0-9]{3})+(?:\.[0-9]+)?", s2):
        s2 = s2.replace(",", "")
    else:
        if "," in s2 and "." not in s2:
            s2 = s2.replace(",", ".")

    s2 = re.sub(r"\s+", "", s2)

    try:
        return float(s2)
    except ValueError:
        return np.nan


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.drop_duplicates()

    df["ingreso_mensual"] = df["ingreso_mensual"].apply(a_numero)
    df["monto_solicitado"] = df["monto_solicitado"].apply(a_numero)

    df["region"] = df["region"].astype("string")
    df["region"] = df["region"].str.strip()
    df["region"] = df["region"].str.replace("Bogotá", "Bogota", regex=False)
    df["region"] = df["region"].str.lower()

    mapa_region = {
        "bogota": "Bogota",
        "antioquia": "Antioquia",
        "valle": "Valle",
        "santander": "Santander",
        "costa": "Costa",
        "costaa": "Costa"
    }
    df["region"] = df["region"].map(mapa_region)

    df["sexo"] = df["sexo"].astype("string")
    df["sexo"] = df["sexo"].str.strip().str.lower()
    mapa_sexo = {"m": "M", "f": "F", "masculino": "M", "femenino": "F"}
    df["sexo"] = df["sexo"].map(mapa_sexo)

    df = df.dropna(subset=["region", "sexo", "ingreso_mensual", "monto_solicitado"])

    df = df[(df["ingreso_mensual"] > 0) & (df["monto_solicitado"] > 0)]

    df["ingreso_mensual"] = df["ingreso_mensual"].round(0).astype(int)
    df["monto_solicitado"] = df["monto_solicitado"].round(0).astype(int)

    return df
