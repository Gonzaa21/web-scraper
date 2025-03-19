import aiohttp
import asyncio
from parse import parser

async def scraper(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response: # Obtain URL with GET
            return await response.text() # Return in HTML

def UserURL():
    undone = True
    print('╔══════════════════════╗\nEnter "done" to finish"\n╚══════════════════════╝\n')
    while undone:
        input_url = input('⤷ Write URL correctly:')
        
        if input_url.lower() == "done":
            undone = False
            break

        with open('urls.txt','a',encoding="UTF-8") as f:
            f.write(input_url + '\n')
            
    print('✔ URLs saved in urls.txt correctly.')

async def main():
    userURL = UserURL()
    # Load URLS
    with open('urls.txt') as file:
        urls = [line.strip() for line in file.readlines()] # Travel URLs lines and delete whitespaces
        
        tasks = [scraper(url) for url in urls]
        htmls = await asyncio.gather(*tasks)  # Execute multiple petitions in same time

        data = [parser(html) for html in htmls]  # Process data scraped
        for dato in data:
            print(dato)

asyncio.run(main())
        