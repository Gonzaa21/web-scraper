import aiohttp
import asyncio
from parse import parser

async def scraper(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response: # Obtain URL with GET
                return await response.text() # Return in HTML
        
        except aiohttp.InvalidURL:
            print(f"\033[31m✘ Invalid URL: {url}\033[0m")
        except aiohttp.ClientError:
            print(f"\033[33m⚠ Error accessing: {url}\033[0m")
        
        return None # Return None in any errors
        
def UserURL():
    undone = True
    print(f'\033[37m╔═══════════════════════╗\033[0m\033[97m\n Enter "done" to finish\n\033[0m\033[37m╚═══════════════════════╝\n\033[0m')
    while undone:
        input_url = input(f'\033[90m⤷ Write URL correctly: \033[0m')
        
        if input_url.lower() == "done":
            undone = False
            break

        with open('urls.txt','a',encoding="UTF-8") as f:
            f.write(input_url + '\n')
            
    
    
async def load_url():
    try:
        with open('urls.txt','r',encoding='UTF-8') as file:
            # delete whitespaces and empty lines
            urls = [line.strip() for line in file if line.strip()]
        
    except FileNotFoundError:
        print('\033[31m✘ No URL file found. Please add URLs first.\033[0m')
    
    # validate if url starts with https
    valid_urls = [url for url in urls if url.startswith(("http://", "https://"))]
    
    if len(valid_urls) < len(urls):
        print("\033[33m⚠ Some invalid URLs were removed.\033[0m")
        # remove invalids urls
        with open('urls.txt', 'w', encoding="UTF-8") as f:
            f.write("\n".join(valid_urls) + '\n')

    return valid_urls
    
async def main():
    UserURL()
    urls = await load_url()
    
    if not urls:
        print("\033[31m✘ No valid URLs to process.\033[0m")
        return
    print('✔ URLs saved in urls.txt correctly.')
    with open('urls.txt') as file: # Load URLS
        urls = [line.strip() for line in file.readlines()] # Travel URLs lines and delete whitespaces

        tasks = [scraper(url) for url in urls]
        htmls = await asyncio.gather(*tasks)  # Execute multiple petitions in same time

        data = [parser(html) for html in htmls]  # Process data scraped
        for dato in data:
            print(dato)

asyncio.run(main())