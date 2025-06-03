import asyncio
from matplotlib import pyplot as plt
from pydantic import BaseModel

from tools.market_share_chart_tool import generate_market_share_pie_chart

class CompanyMarketShare(BaseModel):
    company_name: str
    """Name of the company."""
    
    market_share: int
    """Market share percentage of the company."""
    
class CompanyMarketSharesData(BaseModel):
    market_shares: list[CompanyMarketShare]
    """A list of companies with their respective market shares."""

class PieChartData(BaseModel):
    labels: list[str]
    """Labels for each slice of the pie chart."""
    
    values: list[float]
    """Values corresponding to each label, representing the size of each slice."""
    
    colors: list[str]
    """Colors for each slice of the pie chart."""
    
    explode: list[float]
    """A list indicating the fraction of the radius to offset each slice, for emphasis."""
    
    
company_market_shares = CompanyMarketSharesData(
    market_shares=[
        CompanyMarketShare(company_name="Nike", market_share=40),
        CompanyMarketShare(company_name="Adidas", market_share=30),
        CompanyMarketShare(company_name="Puma", market_share=30),
    ]
)

asyncio.run(generate_market_share_pie_chart(company_market_shares))