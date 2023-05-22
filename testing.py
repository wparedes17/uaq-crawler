import re
import json
import urllib3
from bs4 import BeautifulSoup

# list of attributes:
atrs = ['DC.title', 'DC.creator', 'DC.date', 'DC.description', 'DC.subject', 'DC.type', 'DC.identifier', 'citation_pdf_url']

http = urllib3.PoolManager()
handle = '/handle/123456789/3699'
r = http.request('get', 'https://ri-ng.uaq.mx' + handle)

# Supongamos que tienes el código fuente HTML en la variable 'html_content'
soup = BeautifulSoup(r.data, 'html.parser')
json_docto = {}
for atr in atrs:
    json_docto[atr] = []
    meta_tags = soup.find_all('meta', attrs={'name': atr})
    # Imprime el contenido de las etiquetas encontradas
    for meta_tag in meta_tags:
        print(meta_tag)
        content = meta_tag.get('content')
        json_docto[atr].append(content)

print(json_docto)

