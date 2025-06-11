from agents import Runner
from llm_agents.campaign.agent import campaign_agent, CampaignsList
from llm_agents.search.tools.deep_dive_tool import deep_dive_tool
from llm_agents.csv_maker.agent import csv_maker_agent, CSVResult
from utils import generate_csv_file_from_text

data_input = ""

with open('context.txt', 'r') as file:
    for line in file:
        print(line.strip())
        data_input += line.strip() + " "

prompt = f"""
        Given this data: {data_input}. \n\n
        Generate a CSV file from the given data.
        """

async def main():
    result = await Runner().run(
        csv_maker_agent,
        input=prompt
    )
    csv_agent_output  = result.final_output_as(CSVResult)
    print(csv_agent_output)
    generate_csv_file_from_text(csv_agent_output.csv_file, "campaigns.csv")
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())