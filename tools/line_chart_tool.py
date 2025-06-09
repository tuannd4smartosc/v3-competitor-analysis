from collections import defaultdict
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import BaseModel, model_validator
import uuid
from agents import FunctionTool, RunContextWrapper

class CompanyRevenue(BaseModel):
    company_name: str
    """Name of the company"""

    revenue: int
    """Company's revenue"""

    year: int
    """The year that the revenue is recorded"""
    
    class Config:  
        extra = "forbid"  
    
class CompetitorsRevenueData(BaseModel):
    competitors: list[CompanyRevenue]
    """List of revenue data from multiple competitors"""
    
    class Config:  
        extra = "forbid"  

def convert_to_chart_data(data: CompetitorsRevenueData):
    # Organize by year first for consistent ordering
    sorted_data = sorted(data.competitors, key=lambda x: (x.year, x.company_name))

    # Extract unique years in sorted order
    years = sorted(set(item.year for item in sorted_data))
    
    # Create a dict: { company_name: {year: revenue} }
    temp_data = defaultdict(dict)
    for entry in sorted_data:
        temp_data[entry.company_name][entry.year] = entry.revenue

    # Create company_data: { company_name: [revenue1, revenue2, ...] }
    company_data = {
        company: [yearly_revs.get(year, 0) for year in years]
        for company, yearly_revs in temp_data.items()
    }

    return years, company_data
    
# Convert to DataFrame
async def generate_revenue_line_chart(data: CompetitorsRevenueData):
    years, company_data = convert_to_chart_data(data)
    plt.figure(figsize=(10, 6))

    # Plot each company's data
    for company, values in company_data.items():
        plt.plot(years, values, marker='o', label=company)

    # Add labels, title, legend, and grid
    plt.title("Company Revenue Over Time")
    plt.xlabel("Year")
    plt.ylabel("Revenue (in millions)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"line_chart_{uuid.uuid4().hex}.png", dpi=300, bbox_inches='tight') 
    
async def function_tool_generate_revenue_line_chart(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for generating traffic or revenue analysis line charts"""
    print("args", args)
    chart_data = CompetitorsRevenueData.model_validate_json(args)
    return await generate_revenue_line_chart(chart_data)

line_chart_tool = FunctionTool(
    name="generate_revenue_line_chart",
    description="Generates a line chart visualizing traffic or revenue data between competitors.",
    params_json_schema=CompetitorsRevenueData.model_json_schema(),
    on_invoke_tool=function_tool_generate_revenue_line_chart,
)