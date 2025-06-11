from agents import Runner
from llm_agents.campaign.agent import campaign_agent, CampaignsList
from llm_agents.search.tools.deep_dive_tool import deep_dive_tool
from llm_agents.search.price_search.agent import price_research_agent

async def main():
    result = await Runner().run(
        price_research_agent,
        input="Deep dive into this url: https://www.modernnotoriety.com/story-mfg-asics-gel-venture-6-release-date/ and generate a list of campaigns"
    )
    campaigns  = result.final_output_as(CampaignsList)
    print(campaigns)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())