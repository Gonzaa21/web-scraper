from bs4 import BeautifulSoup
import json
import os

def parser(html): # Extract HTML data
    if not html: return {"ERROR":"Invalid HTML data"}
    soup = BeautifulSoup(html, 'lxml')
    
    # Extract data from website
    title = soup.title.string if soup.title else "Any Title"
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"] if meta_description else "No description"
    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")][:4]
    images = [{"src": img["src"], "alt": img.get("alt", "No alt text")} for img in soup.find_all("img", src=True)]
    
    datajson = {
        title: {
            "title":title,
            "description": description,
            "h1_tags": h1_tags,
            "paragraphs": paragraphs,
            "images": images,
        }
    }
    
    # if json file exist, open url.json
    if os.path.exists("urls.json"):
        with open("urls.json", "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):  # if json is not a list, convert in one
                    existing_data = []
            except json.JSONDecodeError:
                existing_data = [] # In the case of the file is empty
    else:
        existing_data = []

    # add to list
    existing_data.append(datajson)

    # save in urls.json
    with open("urls.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    
    return datajson
