from typing import Any, List, Optional
import uuid
from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import pandas as pd

class Product(BaseModel):
    brand: str
    price: float
    rating: float
    
    class Config:  
        extra = "forbid" 

class BrandPosition(BaseModel):
    brand: str
    average_price: float
    average_rating: float
    
    class Config:  
        extra = "forbid" 

class BrandMovement(BaseModel):
    brand: str
    old_position: BrandPosition
    new_position: BrandPosition
    
    class Config:  
        extra = "forbid" 

class PerceptualMapData(BaseModel):
    products: List[Product]
    brand_positions: List[BrandPosition]
    movements: Optional[List[BrandMovement]] = Field(default=None)
    
    class Config:  
        extra = "forbid" 
    
class ProductList(BaseModel):
    products: list[Product]
    
    class Config:  
        extra = "forbid" 

async def generate_perceptual_map(products_list: ProductList):
    products = products_list.products
    df = pd.DataFrame([p.dict() for p in products])
    brand_avg_df = df.groupby('brand').agg({'price': 'mean', 'rating': 'mean'}).reset_index()
    brand_positions = [
        BrandPosition(brand=row['brand'], average_price=row['price'], average_rating=row['rating'])
        for _, row in brand_avg_df.iterrows()
    ]

    nike_old = BrandPosition(brand="Nike", average_price=140.0, average_rating=3.8)
    nike_new = next(bp for bp in brand_positions if bp.brand == "Nike")
    nike_movement = BrandMovement(brand="Nike", old_position=nike_old, new_position=nike_new)

    map_data = PerceptualMapData(
        products=products,
        brand_positions=brand_positions,
        movements=[nike_movement]
    )


    plt.figure(figsize=(10, 6))

    for bp in map_data.brand_positions:
        if bp.brand != "Nike":
            plt.scatter(bp.average_price, bp.average_rating, s=200, label=bp.brand)
            plt.text(bp.average_price + 1, bp.average_rating, bp.brand, fontsize=12)

    for move in map_data.movements or []:
        plt.plot(
            [move.old_position.average_price, move.new_position.average_price],
            [move.old_position.average_rating, move.new_position.average_rating],
            linestyle='--',
            color='red',
            label=f"{move.brand} Position Change"
        )
        plt.scatter(move.old_position.average_price, move.old_position.average_rating, color='red', s=200, marker='x', label=f"{move.brand} (Old)")
        plt.scatter(move.new_position.average_price, move.new_position.average_rating, color='red', s=200, label=f"{move.brand} (New)")
        plt.text(move.old_position.average_price + 1, move.old_position.average_rating, f"{move.brand} (Old)", color='red', fontsize=12)
        plt.text(move.new_position.average_price + 1, move.new_position.average_rating, f"{move.brand} (New)", color='red', fontsize=12)

    avg_price = df['price'].mean()
    avg_rating = df['rating'].mean()
    plt.axhline(y=avg_rating, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=avg_price, color='gray', linestyle='--', alpha=0.5)

    plt.xlabel("Average Price ($)")
    plt.ylabel("Average Rating")
    plt.title("Perceptual Map of Footwear Brands with Nike's Position Change")
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"perceptual_map_{uuid.uuid4().hex}.png", dpi=300, bbox_inches='tight') 
    

async def function_tool_generate_perceptual_map(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for generating perceptual map for pricing comparisons"""
    products_list = ProductList.model_validate_json(args)
    return await generate_perceptual_map(products_list)

perceptual_map_tool = FunctionTool(
    name="generate_perceptual_map",
    description="Generates a perceptual map visualizing pricing comparisons across competitors versus metrics such as Quality / Customer rating / Revenue.",
    params_json_schema=ProductList.model_json_schema(),
    on_invoke_tool=function_tool_generate_perceptual_map,
)