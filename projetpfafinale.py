import pandas as pd
import matplotlib.pyplot as plt

# 1. Lecture des données
df = pd.read_csv("ventes.csv")

print("Aperçu des données :")
print(df.head())

# 2. Calculs
df["CA_Brut"] = df["Price per Unit"] * df["Quantity"]
df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise (%)"] / 100)
df["TVA"] = df["CA_Net"] * 0.2

# 3. Résultats
ca_total = df["CA_Net"].sum()
print("\nChiffre d'affaires total :", round(ca_total, 2))

best = df.loc[df["CA_Net"].idxmax()]
print("\nProduit le plus rentable :")
print(best[["Transaction ID", "Product Category", "CA_Net"]])

# 4. Analyse
ca_categorie = df.groupby("Product Category")["CA_Net"].sum()
print("\nChiffre d'affaires par catégorie :")
print(ca_categorie)

ca_genre = df.groupby("Gender")["CA_Net"].sum()

df["Date"] = pd.to_datetime(df["Date"])
ca_temps = df.groupby("Date")["CA_Net"].sum()

# 5. Export
df.to_csv("resultats_final.csv", index=False)
print("\nFichier resultats_final.csv créé.")

# 6. Graphiques

# Graphique 1 : CA par catégorie
plt.figure()
ca_categorie.plot(kind="bar")
plt.title("Chiffre d'affaires par catégorie")
plt.xlabel("Catégorie")
plt.ylabel("CA Net")
plt.xticks(rotation=30)

# Graphique 2 : CA par genre
plt.figure()
ca_genre.plot(kind="pie", autopct="%1.1f%%")
plt.title("Répartition du CA par genre")
plt.ylabel("")

# Graphique 3 : évolution dans le temps
plt.figure()
ca_temps.plot(marker="o")
plt.title("Évolution du chiffre d'affaires")
plt.xlabel("Date")
plt.ylabel("CA Net")

plt.show()