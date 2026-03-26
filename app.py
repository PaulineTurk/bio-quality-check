import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

st.title("🧬 QC Pipeline - Expression Génique")

# Upload fichier
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    
    st.subheader("📊 Aperçu des données")
    st.write(df)

    # -------- QC CHECKS --------
    st.subheader("✅ Quality Control")

    # 1. Valeurs manquantes
    missing = df.isnull().sum()
    st.write("🔍 Valeurs manquantes :", missing)

    # 2. Expression négative
    negative_values = df[df["expression"] < 0]
    st.write("⚠️ Expression négative :", negative_values)

    # 3. Duplicats
    duplicates = df[df.duplicated()]
    st.write("📌 Duplicats :", duplicates)

    # 4. Ratio normalisation
    df["ratio"] = df["expression"] / df["housekeeping_gene"]

    st.subheader("🧪 Ratio (expression normalisée)")
    st.write(df[["sample_id", "ratio"]])

    # 5. Outliers (Z-score)
    df["zscore"] = np.abs(stats.zscore(df["expression"], nan_policy='omit'))
    outliers = df[df["zscore"] > 3]

    st.subheader("🚨 Outliers détectés (Z > 3)")
    st.write(outliers)

    # 6. Distribution
    st.subheader("📈 Distribution des expressions")
    fig, ax = plt.subplots()
    df["expression"].hist(ax=ax)
    st.pyplot(fig)

    # 7. QC Summary
    st.subheader("📋 QC Summary")

    issues = []

    if missing.sum() > 0:
        issues.append("Valeurs manquantes détectées")

    if len(negative_values) > 0:
        issues.append("Valeurs négatives détectées")

    if len(outliers) > 0:
        issues.append("Outliers détectés")

    if len(issues) == 0:
        st.success("✅ Données propres")
    else:
        for i in issues:
            st.error(i)

    # 8. Filtrer données propres
    clean_df = df[
        (df["expression"] >= 0) &
        (df["zscore"] <= 3) &
        (~df["expression"].isnull())
    ]

    st.subheader("🧹 Données après QC")
    st.write(clean_df)