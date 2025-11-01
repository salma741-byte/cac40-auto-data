
import yfinance as yf
import pandas as pd

# Définir la période d'étude
START = "2020-01-01"
END = "2025-10-31"

# 🔹 Dictionnaire des 10 grandes entreprises françaises du CAC 40
majors = {
    "MC.PA": "LVMH",
    "TTE.PA": "TotalEnergies",
    "SAN.PA": "Sanofi",
    "AIR.PA": "Airbus",
    "BNP.PA": "BNP Paribas",
    "SU.PA": "Schneider Electric",
    "DSY.PA": "Dassault Systèmes",
    "BN.PA": "Danone",
    "CAP.PA": "Capgemini",
    "CS.PA": "AXA"
}

# 🔹 Fonction pour télécharger les données d'une entreprise
def telecharger_donnees(ticker, nom):
    df = yf.download(ticker, start=START, end=END)[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]  # Aplatir les colonnes
    df = df.reset_index()
    df["Entreprise"] = nom
    return df

# 🔹 Télécharger les données du CAC 40
cac40 = telecharger_donnees("^FCHI", "CAC40")

# 🔹 Télécharger les données de chaque entreprise
dfs = [telecharger_donnees(t, n) for t, n in majors.items()]

# 🔹 Concaténer toutes les données
final_df = pd.concat([cac40] + dfs, ignore_index=True)

# 🔹 Réorganiser les colonnes
final_df = final_df[["Entreprise", "Date", "Open", "High", "Low", "Close", "Volume"]]

# 🔹 Trier par entreprise, puis par date
final_df = final_df.sort_values(by=["Entreprise", "Date"]).reset_index(drop=True)

# 🔹 Nettoyer les valeurs manquantes
final_df = final_df.dropna().copy()

# 🔹 Vérifier les 15 premières lignes
print(f"Jeu de données final : {final_df.shape[0]} lignes, {final_df.shape[1]} colonnes")
print(final_df.head(15))

# 🔹 Sauvegarder les fichiers Excel et CSV
final_df.to_excel("CAC40_10Entreprises_Groupées.xlsx", index=False, engine="openpyxl")
final_df.to_csv("CAC40_10Entreprises_Groupées.csv", index=False, encoding="utf-8")

print(" Fichiers Excel et CSV créés avec succès !")

