from typing import List
from _agents.search import APAWebReference
import datetime

reference_list=[APAWebReference(author=None, year=None, title='Accessories | adidas Singapore', website_name='adidas Singapore', url='https://www.adidas.com.sg/accessories', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=None, title='Lifestyle Accessories | adidas Philippines', website_name='adidas Philippines', url='https://www.adidas.com.ph/lifestyle-accessories', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=None, title='Accessories | adidas Vietnam', website_name='adidas Vietnam', url='https://www.adidas.com.vn/en/accessories', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=2025, title='Sportswear Market Global Outlook & Forecast 2024-2029: Global Sportswear Market Poised for USD 579.96 Billion by 2029, Driven by Sustainability and Athleisure Trends - ResearchAndMarkets.com', website_name='Business Wire', url='https://www.businesswire.com/news/home/20250107131237/en/Sportswear-Market-Global-Outlook-Forecast-2024-2029-Global-Sportswear-Market-Poised-for-USD-579.96-Billion-by-2029-Driven-by-Sustainability-and-Athleisure-Trends---ResearchAndMarkets.com/', access_date=datetime.date(2025, 6, 7)), APAWebReference(author='Anindhitha Maniath', year=2023, title="Why Athleisure's Pulse is Racing in Southeast Asia", website_name='Euromonitor International', url='https://www.euromonitor.com/article/why-athleisures-pulse-is-racing-in-southeast-asia', access_date=datetime.date(2025, 6, 7)), APAWebReference(author='Metro.Style', year=2021, title='The Nike App Launches In Southeast Asia—Here’s Why You Need It On Your Phone, Stat!', website_name='Metro.Style', url='https://metro.style/culture/tech/the-nike-app-launches-in-southeast-asia/30700', access_date=datetime.date(2025, 6, 7)), APAWebReference(author='Globe Telecom', year=2022, title='The Largest Nike Store in Southeast Asia Just Opened in Manila - go!', website_name='Globe Telecom', url='https://www.globe.com.ph/go/shopping-lifestyle/article/largest-nike-store-southeast-asia-manila', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=None, title='Accessories - Southeast Asia | Statista Market Forecast', website_name='Statista', url='https://www.statista.com/outlook/cmo/accessories/southeast-asia', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=None, title='GlobalData Plc: Nike Among Top Brands in the APAC', website_name='GlobeNewswire', url='https://www.globenewswire.com/en/news-release/2022/05/11/2441053/0/en/GlobalData-Plc-Nike-Among-Top-Brands-in-the-APAC-Sportswear-Market-in-2020.html', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=2025, title='US tariffs on Vietnam would be a blow to Nike and other sportswear brands', website_name='Reuters', url='https://www.reuters.com/business/retail-consumer/us-tariffs-vietnam-would-be-blow-nike-other-sportswear-brands-2025-04-01/', access_date=datetime.date(2025, 6, 7)), APAWebReference(author=None, year=2023, title='The World’s Third Largest Sportswear Company May Surprise You', website_name='Business of Fashion', url='https://www.businessoffashion.com/briefings/china/the-worlds-third-largest-sportswear-company-may-surprise-you/', access_date=datetime.date(2025, 6, 7))]


def format_apa_citation(ref: APAWebReference) -> str:
    # Format the author
    author = ref.author if ref.author else ref.website_name
    # Format the year
    year = f"({ref.year})" if ref.year else "(n.d.)"
    # Format access date
    access_str = f"Accessed {ref.access_date.strftime('%B %d, %Y')}." if ref.access_date else ""
    # Combine into APA format
    citation = f"{author}. {year}. *{ref.title}*. {ref.website_name}. {access_str} [https://{ref.url.lstrip('https://')}]"
    return citation

def generate_markdown(reference_list: list[APAWebReference]) -> str:
    citations = [format_apa_citation(ref) for ref in reference_list]
    markdown_text = "\n\n".join(citations)
    return markdown_text

gemerated_markdown = generate_markdown(reference_list)
print("gemerated_markdown",gemerated_markdown)