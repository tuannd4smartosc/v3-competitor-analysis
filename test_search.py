from agents import Runner
from _agents.chart import chart_agent
import asyncio


prompt = """
put for chart generation: 
        Search results:
        ### Country/City: Singapore

**Footwear**

| Country/City | Brand  | Product Name                 | Brief Description          | Original Price (SGD) | Adjusted Price (SGD) | Price Change %                              | Customer Segment     |
|--------------|--------|------------------------------|----------------------------|-----------------------|-----------------------|----------------------------------------------|----------------------|
| Singapore    | Nike   | Air Zoom Pegasus 40          | Lightweight Running Shoe   | 150.00               | 145.00               | <span style="color:green">-3.33%</span>    | Runners             |
| Singapore    | Nike   | Air Max Pulse                | Cushioned Lifestyle Shoe   | 220.00               | 220.00               | <span style="color:gray">0.00%</span>      | Casual Wear         |
| Singapore    | Nike   | ZoomX Vaporfly Next% 3       | Marathon Racing Shoe       | 320.00               | 350.00               | <span style="color:red">+9.38%</span>      | Elite Athletes      |
| Singapore    | Nike   | Court Air Zoom GP Turbo      | Tennis Performance Shoe    | 180.00               | 160.00               | <span style="color:green">-11.11%</span>   | Tennis Players      |
| Singapore    | Nike   | Metcon 8                     | Cross-Training Shoe        | 160.00               | 168.00               | <span style="color:red">+5.00%</span>      | Gym/Training        |
| Singapore    | Adidas | Ultraboost 22                | High Comfort Running Shoe  | 250.00               | 225.00               | <span style="color:green">-10.00%</span>   | Runners             |
| Singapore    | Adidas | Samba Classic                | Iconic Lifestyle Shoe      | 130.00               | 130.00               | <span style="color:gray">0.00%</span>      | Casual Wear         |
| Singapore    | Adidas | Adizero Adios Pro 3          | Marathon Racing Shoe       | 320.00               | 336.00               | <span style="color:red">+5.00%</span>      | Elite Athletes      |
| Singapore    | Adidas | Barricade                    | Tennis Stability Shoe      | 180.00               | 162.00               | <span style="color:green">-10.00%</span>   | Tennis Players      |
| Singapore    | Adidas | Powerlift 5                  | Weightlifting Shoe         | 140.00               | 147.00               | <span style="color:red">+5.00%</span>      | Gym/Training        |
| Singapore    | Puma   | Cali Dream Sand              | Stylish Casual Shoe        | 120.00               | 60.00                | <span style="color:green">-50.00%</span>   | Casual Wear         |
| Singapore    | Puma   | Carina 2.0 Pearls            | Casual Women's Shoe        | 80.00                | 40.00                | <span style="color:green">-50.00%</span>   | Casual Wear         |
| Singapore    | Puma   | Deviate Nitro 2              | Lightweight Running Shoe   | 200.00               | 200.00               | <span style="color:gray">0.00%</span>      | Runners             |
| Singapore    | Puma   | Court Rider 2                | Basketball Shoe            | 160.00               | 176.00               | <span style="color:red">+10.00%</span>     | Basketball Players  |
| Singapore    | Puma   | Fuse 2                       | Functional Training Shoe   | 130.00               | 130.00               | <span style="color:gray">0.00%</span>      | Gym/Training        |
| Singapore    | ASICS  | GEL-NIMBUS 25                | Cushioned Running Shoe     | 220.00               | 220.00               | <span style="color:gray">0.00%</span>      | Runners             |
| Singapore    | ASICS  | GEL-KAYANO 28                | Stable Running Shoe        | 210.00               | 220.00               | <span style="color:red">+4.76%</span>      | Runners             |
| Singapore    | ASICS  | Court FF Novak               | Tennis Shoe                | 190.00               | 209.00               | <span style="color:red">+10.00%</span>     | Tennis Players      |
| Singapore    | ASICS  | Metaspeed Sky+               | Marathon Racing Shoe       | 300.00               | 270.00               | <span style="color:green">-10.00%</span>   | Elite Athletes      |
| Singapore    | ASICS  | GEL-Resolution 9             | Tennis Stability Shoe      | 180.00               | 162.00               | <span style="color:green">-10.00%</span>   | Tennis Players      |

**Apparel**

| Country/City | Brand  | Product Name                | Brief Description       | Original Price (SGD) | Adjusted Price (SGD) | Price Change %                              | Customer Segment   |
|--------------|--------|-----------------------------|-------------------------|-----------------------|-----------------------|----------------------------------------------|--------------------|
| Singapore    | Nike   | Dri-FIT Tee                | Breathable Training Tee| 50.00                | 45.00                | <span style="color:green">-10.00%</span>   | Gym/Training      |
| Singapore    | Nike   | Pro Compression Long Sleeve| Compression Base Layer | 70.00                | 70.00                | <span style="color:gray">0.00%</span>      | Athletes          |
| Singapore    | Nike   | Sportswear Club Fleece     | Casual Hoodie          | 80.00                | 88.00                | <span style="color:red">+10.00%</span>     | Casual Wear       |
| Singapore    | Nike   | Flex Stride Running Shorts | Lightweight Running    | 55.00                | 49.50                | <span style="color:green">-10.00%</span>   | Runners           |
| Singapore    | Nike   | Court Dry Skirt            | Tennis Skirt           | 60.00                | 60.00                | <span style="color:gray">0.00%</span>      | Tennis Players    |
| Singapore    | Adidas | Own The Run Tee            | Running T-Shirt        | 45.00                | 45.00                | <span style="color:gray">0.00%</span>      | Runners           |
| Singapore    | Adidas | Tiro 23 Training Pants     | Training Pants         | 65.00                | 52.00                | <span style="color:green">-20.00%</span>   | Athletes          |
| Singapore    | Adidas | 3-Stripes Hoodie           | Iconic Hoodie          | 75.00                | 82.50                | <span style="color:red">+10.00%</span>     | Casual Wear       |
| Singapore    | Adidas | Club Tennis Skirt          | Tennis Skirt           | 55.00                | 49.50                | <span style="color:green">-10.00%</span>   | Tennis Players    |
| Singapore    | Adidas | Techfit Compression LS Top | Compression Base Layer | 65.00                | 65.00                | <span style="color:gray">0.00%</span>      | Athletes          |
| Singapore    | Puma   | Liga Jersey                | Soccer Jersey          | 40.00                | 36.00                | <span style="color:green">-10.00%</span>   | Soccer Players    |
| Singapore    | Puma   | Essentials Fleece Hoodie   | Casual Hoodie          | 60.00                | 60.00                | <span style="color:gray">0.00%</span>      | Casual Wear       |
| Singapore    | Puma   | Modern Sports Tee          | Performance T-Shirt    | 35.00                | 28.00                | <span style="color:green">-20.00%</span>   | Athletes          |
| Singapore    | Puma   | Train Favorite Tank        | Workout Tank           | 30.00                | 33.00                | <span style="color:red">+10.00%</span>     | Gym/Training      |
| Singapore    | Puma   | Iconic T7 Track Pants      | Heritage Track Pants   | 70.00                | 70.00                | <span style="color:gray">0.00%</span>      | Casual Wear       |
| Singapore    | ASICS  | Tennis GPX Tee             | Tennis T-Shirt         | 45.00                | 40.50                | <span style="color:green">-10.00%</span>   | Tennis Players    |
| Singapore    | ASICS  | Race Seamless LS           | Running Long Sleeve    | 65.00                | 58.50                | <span style="color:green">-10.00%</span>   | Runners           |
| Singapore    | ASICS  | ESNT GPX Hoodie            | Casual Hoodie          | 75.00                | 75.00                | <span style="color:gray">0.00%</span>      | Casual Wear       |
| Singapore    | ASICS  | Silver Split Shorts        | Running Shorts         | 45.00                | 49.50                | <span style="color:red">+10.00%</span>     | Runners           |
| Singapore    | ASICS  | Club Skort                 | Tennis Skirt/Shorts    | 50.00                | 45.00                | <span style="color:green">-10.00%</span>   | Tennis Players    |

**Accessories**

| Country/City | Brand   | Product Name                | Brief Description            | Original Price (SGD) | Adjusted Price (SGD) | Price Change %                              | Customer Segment      |
|--------------|---------|-----------------------------|------------------------------|-----------------------|-----------------------|----------------------------------------------|-----------------------|
| Singapore    | Nike    | Heritage86 Cap             | Classic Baseball Cap         | 25.00                | 25.00                | <span style="color:gray">0.00%</span>       | Casual/All           |
| Singapore    | Nike    | Swoosh Wristbands          | Sweat-Absorbing Wristbands   | 15.00                | 13.50                | <span style="color:green">-10.00%</span>    | Athletes             |
| Singapore    | Nike    | Brasilia Training Duffel   | Medium-Sized Gym Bag         | 50.00                | 55.00                | <span style="color:red">+10.00%</span>      | Gym/Training         |
| Singapore    | Nike    | Essential Ankle Socks      | Basic Ankle Socks (3 Pack)   | 18.00                | 18.00                | <span style="color:gray">0.00%</span>       | All                  |
| Singapore    | Nike    | Gym Essentials Backpack    | Durable Backpack             | 45.00                | 40.50                | <span style="color:green">-10.00%</span>    | Students/Gym         |
| Singapore    | Adidas  | Badge of Sport Cap         | Adjustable Sports Cap        | 25.00                | 22.50                | <span style="color:green">-10.00%</span>    | Casual/All           |
| Singapore    | Adidas  | Tiro Gym Sack              | Lightweight Gym Sack         | 20.00                | 18.00                | <span style="color:green">-10.00%</span>    | Athletes             |
| Singapore    | Adidas  | 3-Stripes Backpack         | Classic Multi-Purpose Bag    | 35.00                | 31.50                | <span style="color:green">-10.00%</span>    | Students/Gym         |
| Singapore    | Adidas  | Tennis Wristband (Double)  | Absorbent Tennis Wristbands  | 15.00                | 15.00                | <span style="color:gray">0.00%</span>       | Tennis Players       |
| Singapore    | Adidas  | Running Waist Pack         | Reflective Belt Bag          | 30.00                | 33.00                | <span style="color:red">+10.00%</span>      | Runners              |
| Singapore    | Puma    | Phase Backpack             | Simple Training Backpack     | 30.00                | 27.00                | <span style="color:green">-10.00%</span>    | Students/Athletes    |
| Singapore    | Puma    | Performance Cap            | Moisture-Wicking Cap         | 25.00                | 25.00                | <span style="color:gray">0.00%</span>       | Athletes             |
| Singapore    | Puma    | Fundamentals Grip Bag      | Durable Sports Duffel        | 45.00                | 40.50                | <span style="color:green">-10.00%</span>    | Gym/Training         |
| Singapore    | Puma    | Training Wristbands        | Absorbent Wristbands         | 12.00                | 12.00                | <span style="color:gray">0.00%</span>       | All                  |
| Singapore    | Puma    | Team Final Pro Ball        | Match-Quality Soccer Ball    | 60.00                | 66.00                | <span style="color:red">+10.00%</span>      | Soccer Players       |
| Singapore    | ASICS   | Running Cap                | Breathable Running Cap       | 25.00                | 25.00                | <span style="color:gray">0.00%</span>       | Runners              |
| Singapore    | ASICS   | Training Waist Pouch       | Convenient Running Belt      | 28.00                | 25.20                | <span style="color:green">-10.00%</span>    | Runners              |
| Singapore    | ASICS   | Tennis Backpack            | Racquet Compartment Bag      | 60.00                | 60.00                | <span style="color:gray">0.00%</span>       | Tennis Players       |
| Singapore    | ASICS   | Water Bottle               | BPA-Free Bottle              | 15.00                | 16.50                | <span style="color:red">+10.00%</span>      | All                  |
| Singapore    | ASICS   | Performance Socks (3-Pack) | Cushioned Socks             | 18.00                | 18.00                | <span style="color:gray">0.00%</span>       | Athletes             |

**Local Price Comparison Summaries (Singapore)**

a. Average Price per Brand (All Segments)

| Country/City | Brand   | Average Original Price (SGD) | Average Adjusted Price (SGD) | Average Price Change %                       |
|--------------|---------|------------------------------|------------------------------|----------------------------------------------|
| Singapore    | Nike    | 100.00                       | 102.50                       | <span style="color:red">+2.50%</span>        |
| Singapore    | Adidas  | 95.00                        | 90.25                        | <span style="color:green">-5.00%</span>      |
| Singapore    | Puma    | 80.00                        | 80.00                        | <span style="color:gray">0.00%</span>         |
| Singapore    | ASICS   | 110.00                       | 99.00                        | <span style="color:green">-10.00%</span>     |

b. Highest and Lowest Priced Items per Brand

| Country/City | Brand   | Highest Priced Item (SGD) | Lowest Priced Item (SGD) |
|--------------|---------|---------------------------|--------------------------|
| Singapore    | Nike    | 350.00                    | 13.50                    |
| Singapore    | Adidas  | 336.00                    | 15.00                    |
| Singapore    | Puma    | 176.00                    | 12.00                    |
| Singapore    | ASICS   | 300.00                    | 15.00                    |

c. Price Spread (Standard Deviation) per Brand

| Country/City | Brand   | Price Standard Deviation (SGD) |
|--------------|---------|---------------------------------|
| Singapore    | Nike    | 65.00                           |
| Singapore    | Adidas  | 58.00                           |
| Singapore    | Puma    | 42.00                           |
| Singapore    | ASICS   | 70.00                           |

---

### Country/City: Malaysia

**Footwear**

| Country/City | Brand  | Product Name            | Brief Description        | Original Price (MYR) | Adjusted Price (MYR) | Price Change %                              | Customer Segment     |
|--------------|--------|-------------------------|--------------------------|-----------------------|-----------------------|----------------------------------------------|----------------------|
| Malaysia     | Nike   | Air Zoom Pegasus 40     | Lightweight Running Shoe | 500.00               | 475.00               | <span style="color:green">-5.00%</span>     | Runners             |
| Malaysia     | Nike   | Air Max Pulse           | Cushioned Lifestyle Shoe | 650.00               | 650.00               | <span style="color:gray">0.00%</span>       | Casual Wear         |
| Malaysia     | Nike   | ZoomX Vaporfly Next% 3  | Marathon Racing Shoe     | 950.00               | 997.50               | <span style="color:red">+5.00%</span>       | Elite Athletes      |
| Malaysia     | Nike   | Court Air Zoom GP Turbo | Tennis Performance Shoe  | 550.00               | 522.50               | <span style="color:green">-5.00%</span>     | Tennis Players      |
| Malaysia     | Nike   | Metcon 8                | Cross-Training Shoe      | 520.00               | 520.00               | <span style="color:gray">0.00%</span>       | Gym/Training        |
| Malaysia     | Adidas | Ultraboost 22           | High Comfort Running Shoe| 700.00               | 735.00               | <span style="color:red">+5.00%</span>       | Runners             |
| Malaysia     | Adidas | Samba Classic           | Iconic Lifestyle Shoe    | 400.00               | 400.00               | <span style="color:gray">0.00%</span>       | Casual Wear         |
| Malaysia     | Adidas | Adizero Adios Pro 3     | Marathon Racing Shoe     | 950.00               | 950.00               | <span style="color:gray">0.00%</span>       | Elite Athletes      |
| Malaysia     | Adidas | Barricade               | Tennis Stability Shoe    | 500.00               | 525.00               | <span style="color:red">+5.00%</span>       | Tennis Players      |
| Malaysia     | Adidas | Powerlift 5             | Weightlifting Shoe       | 420.00               | 399.00               | <span style="color:green">-5.00%</span>     | Gym/Training        |
| Malaysia     | Puma   | Cali Dream Sand         | Stylish Casual Shoe      | 350.00               | 175.00               | <span style="color:green">-50.00%</span>    | Casual Wear         |
| Malaysia     | Puma   | Carina 2.0 Pearls       | Casual Women's Shoe      | 220.00               | 143.00               | <span style="color:green">-35.00%</span>    | Casual Wear         |
| Malaysia     | Puma   | Deviate Nitro 2         | Lightweight Running Shoe | 450.00               | 450.00               | <span style="color:gray">0.00%</span>       | Runners             |
| Malaysia     | Puma   | Court Rider 2           | Basketball Shoe          | 380.00               | 399.00               | <span style="color:red">+5.00%</span>       | Basketball Players  |
| Malaysia     | Puma   | Fuse 2                  | Functional Training Shoe | 320.00               | 304.00               | <span style="color:green">-5.00%</span>     | Gym/Training        |
| Malaysia     | ASICS  | GEL-NIMBUS 25           | Cushioned Running Shoe   | 690.00               | 690.00               | <span style="color:gray">0.00%</span>       | Runners             |
| Malaysia     | ASICS  | GEL-KAYANO 28           | Stable Running Shoe      | 680.00               | 646.00               | <span style="color:green">-5.00%</span>     | Runners             |
| Malaysia     | ASICS  | Court FF Novak          | Tennis Shoe              | 620.00               | 651.00               | <span style="color:red">+5.00%</span>       | Tennis Players      |
| Malaysia     | ASICS  | Metaspeed Sky+          | Marathon Racing Shoe     | 880.00               | 792.00               | <span style="color:green">-10.00%</span>    | Elite Athletes      |
| Malaysia     | ASICS  | GEL-Resolution 9        | Tennis Stability Shoe    | 600.00               | 600.00               | <span style="color:gray">0.00%</span>       | Tennis Players      |

**Local Price Comparison Summaries (Malaysia)**

a. Average Price per Brand (All Segments)

| Country/City | Brand   | Average Original Price (MYR) | Average Adjusted Price (MYR) | Average Price Change %                       |
|--------------|---------|------------------------------|------------------------------|----------------------------------------------|
| Malaysia     | Nike    | 634.00                       | 632.50                       | <span style="color:green">-0.24%</span>      |
| Malaysia     | Adidas  | 610.00                       | 615.00                       | <span style="color:red">+0.82%</span>        |
| Malaysia     | Puma    | 344.00                       | 294.20                       | <span style="color:green">-14.48%</span>     |
| Malaysia     | ASICS   | 694.00                       | 675.80                       | <span style="color:green">-2.62%</span>      |

b. Highest and Lowest Priced Items per Brand

| Country/City | Brand   | Highest Priced Item (MYR) | Lowest Priced Item (MYR) |
|--------------|---------|---------------------------|--------------------------|
| Malaysia     | Nike    | 997.50                    | 475.00                   |
| Malaysia     | Adidas  | 950.00                    | 399.00                   |
| Malaysia     | Puma    | 450.00                    | 143.00                   |
| Malaysia     | ASICS   | 880.00                    | 600.00                   |

c. Price Spread (Standard Deviation) per Brand

| Country/City | Brand   | Price Standard Deviation (MYR) |
|--------------|---------|---------------------------------|
| Malaysia     | Nike    | 75.00                           |
| Malaysia     | Adidas  | 58.00                           |
| Malaysia     | Puma    | 92.00                           |
| Malaysia     | ASICS   | 80.00                           |


(*Repeat the above structure—Product Segment Analysis tables and all three Local Price Comparison Summaries—for each remaining country or major city in Southeast Asia.*)

        From the search results above, generate a separate heatmap for each country found in the following search results. 
        Each heatmap should display the discount rates of products grouped by their country of origin.
        The heatmap should have product names or brands on one axis and their respective discount percentages on the other.
        For each product, use the following attributes:

        - Product name
        - Brand
        - Original price
        - Discounted price
        - Location (country of origin)

        Calculate the discount rate as a percentage:
            - Discount Rate = (Original Price - Discounted Price) / Original Price × 100%

        Display one heat map where each cell represents a product, grouped by brand, with color intensity indicating the discount rate. Use clear labeling to identify products and their respective brands.
        
"""

async def run():
    result = await Runner.run(
        chart_agent,
        prompt,
    )
    print(result.final_output_as(str))
    
if __name__ == "__main__":
    asyncio.run(run())