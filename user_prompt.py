
# Generate prompt function from your original script
def generate_prompt(company_name: str, competitor_names: str, date: str, region: str) -> str:
    return (
        f"""
        Generate a comprehensive competitor analysis report for **{company_name}** versus **{competitor_names}** in **{region}** 
        for the date range: **{date}**. 

        The report must focus on the **promotional campaigns** of both {company_name} and its competitors. 
        
        Finally, based on your analysis, suggest **a strategic action plan** for {company_name} to improve its market position and campaign effectiveness in {region}.
        """
    )