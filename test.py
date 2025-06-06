# import uuid
# import matplotlib.pyplot as plt
# from openai import BaseModel
# import seaborn as sns
# import pandas as pd

# # Data from Footwear table

# class Product(BaseModel):
#     brand: str
#     """Brand name of the product"""
    
#     product: str
#     """Product name"""
    
#     original_price: float
#     """Product's original price before any discount or promotion"""
    
#     discounted_price: float
#     """Product's final price after discount or promotion"""
    
# class ProductList(BaseModel):
#     products: list[Product]
#     """List of products used to generate the price comparison chart"""


# def generate_heat_map(products_list: ProductList):
#     data = [[p.brand, p.product, p.original_price, p.discounted_price] for p in products_list.products]

#     # Convert to DataFrame
#     df = pd.DataFrame(data, columns=["Brand", "Product", "Original", "Discounted"])
#     df["Discount"] = df["Original"] - df["Discounted"]

#     # Pivot table for heatmap
#     pivot = df.pivot(index="Brand", columns="Product", values="Discount")

#     # Plot heatmap
#     plt.figure(figsize=(12, 6))
#     sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.5, cbar_kws={"label": "Discount (USD)"})
#     plt.title("Footwear Discount Heatmap (Original - Discounted Price)")
#     plt.ylabel("Brand")
#     plt.xlabel("Product")
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(f"charts/heat_map_{uuid.uuid4().hex}.png", dpi=300, bbox_inches='tight') 

# products_list = ProductList(
#     products=[
#         Product(brand="Nike", product="Air VaporMax 2023", original_price=210, discounted_price=180),
#         Product(brand="Adidas", product="Ultraboost 22", original_price=190, discounted_price=170),
#         Product(brand="Lululemon", product="Chargefeel Low", original_price=120, discounted_price=110),
#         Product(brand="Skechers", product="Max Cushioning", original_price=90, discounted_price=80),
#         Product(brand="Nike", product="React Infinity Run", original_price=150, discounted_price=130),
#         Product(brand="Adidas", product="NMD R1", original_price=140, discounted_price=120),
#         Product(brand="Lululemon", product="Blissfeel", original_price=150, discounted_price=140),
#         Product(brand="Skechers", product="Go Walk 5", original_price=80, discounted_price=75),
#         Product(brand="Nike", product="Pegasus 38", original_price=120, discounted_price=100),
#         Product(brand="Adidas", product="Stan Smith", original_price=100, discounted_price=90),
#         Product(brand="Puma", product="test", original_price=222, discounted_price=98),
#     ]
# )

# generate_heat_map(products_list)\

from utils import get_first_temp_filename


chart_filename = get_first_temp_filename("temp")
print("chart_filename", chart_filename)