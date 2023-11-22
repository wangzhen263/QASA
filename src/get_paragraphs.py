from bs4 import BeautifulSoup
import bs4
import requests
import json
import re
    
class PaperDownloadException(Exception):
    def __init__(self, link, message):
        self.link = link
        self.message = message
        super().__init__(self.message)

def parsing_paragraph(link):

    response = requests.get(link, verify=False)
    html = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")

    do_print_abstract = False
    # Find paper title
    try:
        raw_title = soup.find_all("h1", "ltx_title ltx_title_document")
        if len(raw_title) > 0:
            text_title = raw_title[0].text
        else:
            raw_title = soup.find_all("span", "ltx_text ltx_font_bold")
            text_title = raw_title[0].text
            do_print_abstract = True
    except IndexError:
        print('IndexError title: ', link)
        text_title = ""
        do_print_abstract = True

    # Find paper auther information
    try:
        raw_author_info = soup.find_all("span", "ltx_personname")[0]
        authors_list = [item.strip() for item in raw_author_info.children if isinstance(item, bs4.element.NavigableString)]
        authors_list = list(filter(None, authors_list))
        authors_text = ', '.join(authors_list)
    except IndexError:
        authors_text = ""
        do_print_abstract = True

    # Find all sections with an id attribute that contains the letter "S"
    try:
        raw_abstract = soup.find_all("div", "ltx_abstract")
        abstract = ''.join(raw_abstract[0].text.split("\n")[2:])
        if do_print_abstract:
            print(link)
            print(abstract)


        sections = soup.find_all("section", attrs={"id": re.compile(r"^S\d+$")})
        subsections = soup.find_all(class_= 'ltx_para', id=re.compile(r"^S\d+\.+(p|S)"))

        # Count the number of sections
        count = len(subsections)

        paragraphs = []
        section_names = []
        for i in range(count):
            paragraphs.append(re.sub(r"\n", "", subsections[i].text))
    except IndexError:
        raise PaperDownloadException(link, "Failed to download the paragraph data")

    return text_title, authors_text, abstract, paragraphs

"""
if __name__=='__main__':

    arxiv_ids = ['2105.06323'] # https://arxiv.org/abs/2105.06323
    ar5iv_links = []
    for arxiv_id in arxiv_ids:
        ar5iv_links.append(f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}")
    text_title, authors_text, abstract, paragraphs = parsing_paragraph(ar5iv_links[0])
"""
