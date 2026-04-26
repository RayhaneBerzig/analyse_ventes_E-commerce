import pandas as pd
import matplotlib.pyplot as plt
import csv
import random
from datetime import datetime, timedelta

# =========================
# 1. Génération automatique du fichier ventes.csv
# =========================
with open("ventes.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # En-têtes
    writer.writerow([
        "Transaction ID", "Date", "Customer ID", "Gender",
        "Product Category", "Quantity", "Price per Unit", "Remise (%)"
    ])

    categories = ["Clothing", "Beauty", "Electronics"]
    genders = ["Male", "Female"]

    start_date = datetime(2023, 1, 1)

    # Générer 20 lignes automatiquement
    for i in range(1, 21):
        date = start_date + timedelta(days=i)

        writer.writerow([
            i,
            date.strftime("%Y-%m-%d"),
            f"CUST{i}",
            random.choice(genders),
            random.choice(categories),
            random.randint(1, 5),
            random.randint(20, 200),
            random.choice([0, 5, 10, 15, 20])
        ])

print("✅ Fichier ventes.csv généré automatiquement.")

# =========================
# 2. Lecture des données
# =========================
df = pd.read_csv("ventes.csv")

print("\nAperçu des données :")
print(df.head())

# =========================
# 3. Calculs
# =========================
df["CA_Brut"] = df["Price per Unit"] * df["Quantity"]
df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise (%)"] / 100)
df["TVA"] = df["CA_Net"] * 0.2

# =========================
# 4. Résultats
# =========================
ca_total = df["CA_Net"].sum()
print("\nChiffre d'affaires total :", round(ca_total, 2))

best = df.loc[df["CA_Net"].idxmax()]
print("\nProduit le plus rentable :")
print(best[["Transaction ID", "Product Category", "CA_Net"]])

# =========================
# 5. Analyse
# =========================
ca_categorie = df.groupby("Product Category")["CA_Net"].sum()
ca_genre = df.groupby("Gender")["CA_Net"].sum()

df["Date"] = pd.to_datetime(df["Date"])
ca_temps = df.groupby("Date")["CA_Net"].sum().sort_index()

print("\nCA par catégorie :")
print(ca_categorie)

print("\nCA par genre :")
print(ca_genre)

# =========================
# 6. Export final
# =========================
df.to_csv("resultats_final.csv", index=False)
print("\n✅ Fichier resultats_final.csv créé.")

# =========================
# 7. Graphiques
# =========================

# Graphique 1 : CA par catégorie
plt.figure(figsize=(8,5))
ca_categorie.plot(kind="bar", color="skyblue")
plt.title("Chiffre d'affaires par catégorie")
plt.xlabel("Catégorie")
plt.ylabel("CA Net")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graphique_categorie.png")

# Graphique 2 : CA par genre
plt.figure(figsize=(6,6))
ca_genre.plot(kind="pie", autopct="%1.1f%%")
plt.title("Répartition du CA par genre")
plt.ylabel("")
plt.tight_layout()
plt.savefig("graphique_genre.png")

# Graphique 3 : évolution temporelle
plt.figure(figsize=(8,5))
ca_temps.plot(marker="o", color="green")
plt.title("Évolution du chiffre d'affaires")
plt.xlabel("Date")
plt.ylabel("CA Net")
plt.grid()
plt.tight_layout()
plt.savefig("graphique_temps.png")

plt.show()