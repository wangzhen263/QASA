import os
import json
from get_paragraphs import *

DATA_JSON_FILE = os.environ.get("DATA_FILE", "data/testset_answerable_1554_v1.1.json")
with open(DATA_JSON_FILE, 'r') as f:
    data = json.load(f)

all_papers = {}
no_arxiv = []
for idx, d in data.items():
    paper_id = d["paper_id"]
    if paper_id not in all_papers:
        try:
            all_papers[paper_id] = d["arxiv_id"] 
        except KeyError:
            no_arxiv.append(d)

print(f"SKIP {len(no_arxiv)} papers because they do not have arxiv url. ")
print(f"Will download {len(all_papers)} papers from arxiv")

for idx, arxiv_id in all_papers.items():
    ar5iv_link = f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}"
    try:
        text_title, authors_text, abstract, paragraphs = parsing_paragraph(ar5iv_link)
    except PaperDownloadException as e:
        print("## ", e)
        continue

    with open(f"downloads/{idx}.txt", "w") as f:
        f.write(text_title + "\n")
        f.write(authors_text + "\n")
        f.write(abstract + "\n")

        for p in paragraphs:
            f.write(p + "\n")
