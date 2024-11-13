import aiohttp
import asyncio
import os 

async def image_dl(session, url):
    async with session.get(url, ssl = False) as response:
        content = await response.read()
        with open('drop.jpg', 'wb') as f:
            f.write(content)
        return content

async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['']
        
        print(os.path.join('imgs', 'hilo1'))
        tasks = [image_dl(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
        
asyncio.run(main())   


    
