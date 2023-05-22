import re
import json
import urllib3
from bs4 import BeautifulSoup

# This is the pattern of the links that we want to get
# /handle/123456789/123456789
pattern_handle = re.compile(r'/handle/[0-9]+/[0-9]+')

# Doctos has the following relevant attributes:
atrs = ['DC.title', 'DC.creator', 'DC.date', 'DC.description', 'DC.subject', 'DC.type', 'DC.identifier', 'citation_pdf_url']

# hhtp is a PoolManager object for make requests
http = urllib3.PoolManager()

# This show a simple request to UAQs repository
def main_surfing(n, links):
    r = http.request('get', 'https://ri-ng.uaq.mx/simple-search?query=&sort_by=score&order=desc&rpp=100&etal=0&start=' + str(n))
    soup = BeautifulSoup(r.data, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and pattern_handle.match(href):
            links.append(href)

    return links

# This show a simple request to UAQs repository
def document_web(handle):
    r = http.request('get', 'https://ri-ng.uaq.mx' + handle)
    soup = BeautifulSoup(r.data, 'html.parser')
    docto_id = handle.split('/')[-1]
    json_docto = {'id': docto_id}
    for atr in atrs:
        json_docto[atr] = []
        meta_tags = soup.find_all('meta', attrs={'name': atr})

        for meta_tag in meta_tags:
            if 'content' in meta_tag:
                content = meta_tag['content']
                json_docto[atr].append(content)
            else:
                content = meta_tag.get('content')
                json_docto[atr].append(content)

    return json_docto

def get_file(url, filename):
    r = http.request('get', url)

    with open('doctos/'+filename+'.pdf', 'wb') as file:
        file.write(r.data)


# This is the main function
if __name__ == '__main__':
    links = []
    docto_data_json = []
    # Range is 77 because we know that there are between 7600 and 7700 links
    # number was checked manually
    #for i in range(77):
    #    links = main_surfing(i * 100, links)
    #    print('Page ' + str(i + 1) + ' done')

    # This save the links in a json file
    # Only for backup
    #with open('links.json', 'w') as outfile:
    #    json.dump(links, outfile)
    
    #load links from json file
    with open('links.json') as json_file:
        links = json.load(json_file)

    # This get the data of each document
    flag = False
    for link in links:
        print('Document ' + link + ' started')
        docto_data_json.append(document_web(link))
        print('Document ' + link + ' done')

    # This save the links in a json file
    # Only for backup
    with open('doctos_data.json', 'w') as outfile:
        json.dump(docto_data_json, outfile)
    
    for docto in docto_data_json:
        download_link = docto['citation_pdf_url'][0]
        filename = docto['id']
        get_file(download_link, filename)
        print('File ' + filename + ' done')

    




    