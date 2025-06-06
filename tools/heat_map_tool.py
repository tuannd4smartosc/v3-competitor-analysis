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
    """Brand name of the product"""
    
    product: str
    """Product name that is launched in the campaign. (e.g. Nike Air Max 2025, Jordan 1)"""
    
    original_price: float
    """Product's original price before any discount or promotion"""
    
    discounted_price: float
    """Product's final price after discount or promotion"""
    
    class Config:  
        extra = "forbid"
    
class ProductList(BaseModel):
    products: list[Product]
    """List of products used to generate the price comparison chart"""
    
    class Config:  
        extra = "forbid"


async def generate_heat_map(products_list: ProductList):
    data = [[p.brand, p.product, p.original_price, p.discounted_price] for p in products_list.products]
    
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
    plt.savefig(f"temp/heat_map_{uuid.uuid4().hex}.png", dpi=300, bbox_inches='tight') 

async def function_tool_generate_heat_map(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for generating heat map for pricing comparisons regarding Brand, Product, Original Price and Discounted Price"""
    products_list = ProductList.model_validate_json(args)
    return await generate_heat_map(products_list)

heat_map_tool = FunctionTool(
    name="generate_heat_map",
    description="Generates a heat map visualizing pricing comparisons across competitors versus metrics including Brand, Product, Original Price and Discounted Price.",
    params_json_schema=ProductList.model_json_schema(),
    on_invoke_tool=function_tool_generate_heat_map,
)