import requests
import time
from bs4 import BeautifulSoup as bs


start = time.perf_counter()
urls = ['https://www.hispasexy.org/cl'] + [f'https://www.hispasexy.org/cl/{i}.html' for i in range(1, 8)]

for url in urls:
    response = requests.get(url)
    html = response.text
    soup = bs(html, 'html.parser')
    texto = soup.find_all('blockquote')
    [print(quotes) for quotes in texto]


end = time.perf_counter()
print(f'El programa tardo {end - start} segundos')
