from bs4 import BeautifulSoup
import httpx


def test_get_odoo_url_database():
    with httpx.Client() as client:
        resp = client.get(url='http://runbot.odoo.com/runbot')
    
    soup = BeautifulSoup(resp.text, features='html.parser')
    tags = soup.find_all("td", class_="bg-success-light")

    urls = []
    
    for tag in tags:
        try:
            url = tag.div.div.find('a', title='Sign in on this build')['href']
            url_parts = url.split('?db=')
            if len(url_parts) == 2:
                urls.append([url_parts[0], url_parts[1]])
        except:
            pass

    return urls
    

