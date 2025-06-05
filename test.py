import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data from Footwear table

data = [
    ["Nike", "Air VaporMax 2023", 210, 180],
    ["Adidas", "Ultraboost 22", 190, 170],
    ["Lululemon", "Chargefeel Low", 120, 110],
    ["Skechers", "Max Cushioning", 90, 80],
    ["Nike", "React Infinity Run", 150, 130],
    ["Adidas", "NMD R1", 140, 120],
    ["Lululemon", "Blissfeel", 150, 140],
    ["Skechers", "Go Walk 5", 80, 75],
    ["Nike", "Pegasus 38", 120, 100],
    ["Adidas", "Stan Smith", 100, 90],
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Brand", "Product", "Original", "Discounted"])
df["Discount"] = df["Original"] - df["Discounted"]

# Pivot table for heatmap
pivot = df.pivot(index="Brand", columns="Product", values="Discount")

# Plot heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.5, cbar_kws={"label": "Discount (USD)"})
plt.title("Footwear Discount Heatmap (Original - Discounted Price)")
plt.ylabel("Brand")
plt.xlabel("Product")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
