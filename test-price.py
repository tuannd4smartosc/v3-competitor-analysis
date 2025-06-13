from agents import Runner
from llm_agents.campaign.agent import campaign_agent, CampaignsList
from llm_agents.search.tools.deep_dive_tool import deep_dive_tool
from llm_agents.search.price_search.agent import price_research_agent

async def main():
    result = await Runner().run(
        price_research_agent,
        input="Collect all price information for Nike and Adidas in Southeast"
    )
    campaigns  = result.final_output_as(CampaignsList)
    print(campaigns)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())