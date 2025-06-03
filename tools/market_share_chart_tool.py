from typing import Any
from agents import FunctionTool, RunContextWrapper
from matplotlib import pyplot as plt
from pydantic import BaseModel

class CompanyMarketShare(BaseModel):
    company_name: str
    """Name of the company."""
    
    market_share: int
    """Market share percentage of the company."""
    
    class Config:  # For Pydantic v1
        extra = "forbid"  # Disallow extra fields
    
class CompanyMarketSharesData(BaseModel):
    market_shares: list[CompanyMarketShare]
    """A list of companies with their respective market shares."""
    
    class Config:  # For Pydantic v1
        extra = "forbid"  # Disallow extra fields

class PieChartData(BaseModel):
    labels: list[str]
    """Labels for each slice of the pie chart."""
    
    values: list[float]
    """Values corresponding to each label, representing the size of each slice."""
    
    colors: list[str]
    """Colors for each slice of the pie chart."""
    
    explode: list[float]
    """A list indicating the fraction of the radius to offset each slice, for emphasis."""
    
    class Config: 
        extra = "forbid"
    
class PieChartResponse(BaseModel):
    """Response model for the pie chart generation."""
    image_path: str
    """Path to the generated pie chart image."""
    
    description: str
    """Description of the pie chart, including the data it represents. Should be one or two sentences long."""


async def generate_market_share_pie_chart(company_market_shares: CompanyMarketSharesData):
    """Generates a pie chart visualizing the market shares of different companies."""
    pie_labels = [company.company_name for company in company_market_shares.market_shares]
    pie_values = [company.market_share for company in company_market_shares.market_shares]

    market_share_data = PieChartData(
        labels=pie_labels,
        values=pie_values,
        explode=[0.0] * len(pie_labels),
    )

    plt.pie(market_share_data.values, labels=market_share_data.labels, explode=market_share_data.explode, 
            autopct='%1.1f%%', startangle=140)

    plt.title('Market Share in Footwear Industry')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.
    plt.savefig("pie_chart.png", dpi=300, bbox_inches='tight') 
    return "pie_chart.png"

async def function_tool_generate_market_share_pie_chart(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool to generate a market share pie chart."""
    company_market_shares = CompanyMarketSharesData.model_validate_json(args)
    return await generate_market_share_pie_chart(company_market_shares)

market_share_chart_tool = FunctionTool(
    name="generate_market_share_pie_chart",
    description="Generates a pie chart visualizing the market shares of different companies.",
    on_invoke_tool=generate_market_share_pie_chart,
    params_json_schema=CompanyMarketSharesData.model_json_schema(),
)