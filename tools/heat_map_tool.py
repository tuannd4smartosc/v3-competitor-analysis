from typing import Any
import uuid
from agents import FunctionTool, RunContextWrapper
import matplotlib.pyplot as plt
from openai import BaseModel
import seaborn as sns
import pandas as pd

# Data from Footwear table

class Product(BaseModel):
    brand: str
    """Brand name of the product provided from the search results (e.g. Nike, Adidas, Puma, etc.)"""
    
    product: str
    """Product name or identifier (e.g. Nike Air Max, Adidas Ultraboost). Shorten to 15 characters if necessary."""
    
    original_price: float
    """Product's original price before any discount or promotion"""
    
    discounted_price: float
    """Product's final price after discount or promotion"""
    
    class Config:  
        extra = "forbid"
    
class ProductList(BaseModel):
    products: list[Product]
    """List of products used to generate the price comparison chart"""
    
    location: str
    """Location where the products are sold. (e.g. Singapore, Malaysia, Indonesia, Kuala Lumpur, Beijing, Hanoi, etc.)"""
    
    class Config:  
        extra = "forbid"


async def generate_heat_map(products_list: ProductList):
    data = [[p.brand, p.product, p.original_price, p.discounted_price] for p in products_list.products]
    print("📊 Input data:", data)

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Brand", "Product", "Original", "Discounted"])

    # Calculate % change
    df["Price Change (%)"] = ((df["Discounted"] - df["Original"]) / df["Original"]) * 100

    # Pivot table for heatmap values
    pivot = df.pivot(index="Brand", columns="Product", values="Price Change (%)")

    # Format labels with plus signs for increases
    pivot_display = pivot.applymap(lambda x: f"+{x:.0f}%" if x > 0 else f"{x:.0f}%")

    # Plot heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        pivot,
        annot=pivot_display,
        fmt="",
        cmap="RdYlGn_r",
        center=0,
        vmin=-20,  # Set how far green goes (e.g., -20% discount)
        vmax=10,   # Set how soon red appears (e.g., any increase above 0 up to +10%)
        linewidths=0.5,
        cbar_kws={"label": "Price Change (%)"}
    )

    plt.title(f"Price change across products and brands in {products_list.location}")
    plt.ylabel("Brand")
    plt.xlabel("Product")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    file_name = f"temp/heat_map_{uuid.uuid4().hex}.png"
    print("🖼️ File name of chart:", file_name)
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    return file_name

async def function_tool_generate_heat_map(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for generating heat map for pricing comparisons regarding Brand, Product, Original Price and Discounted Price"""
    products_list = ProductList.model_validate_json(args)
    return await generate_heat_map(products_list)

heat_map_tool = FunctionTool(
    name="generate_heat_map",
    description="Generates a heat map visualizing discount rate comparisons across brands for each country/city within the specified region and date range versus metrics including Brand, Product, Original Price and Discounted Price.",
    params_json_schema=ProductList.model_json_schema(),
    on_invoke_tool=function_tool_generate_heat_map,
)