from bs4 import BeautifulSoup

def parser(html): # Extract HTML data
    if not html: return {"ERROR":"Invalid HTML data"}
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title.string if soup.title else "Any Title"
    return {"title": title}
