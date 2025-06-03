from pydantic import BaseModel


class CompanyPerformance(BaseModel):
    company_name: str
    """Name of the company."""
    
    sales_revenue: float
    """Sales revenue of the company in millions."""
    
    class Config:  # For Pydantic v1
        extra = "forbid"  # Disallow extra fields