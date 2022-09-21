import glob
import bibtexparser
import requests
from bibtexparser.bparser import BibTexParser
from typing import List
from tqdm import tqdm
from time import sleep
import csv

class ReferredPaper(object):
    def __init__(self, article_title, doi):
        self.article_title = article_title
        self.doi = doi

    def __str__(self):
        return f"name: {self.article_title}  doi:{self.doi}"

    @staticmethod
    def get_doi(referred_paper: dict):
        return referred_paper.get("DOI", None)

    @staticmethod
    def get_article_title(referred_paper: dict):
        '''
        obtain article title from different format json
        :param referred_paper: json string obtained from crossref api: https://api.crossref.org/v1/works/ and paper doi
        in key reference. don't have a fixed format
        :return: article_title:str or None
        '''
        # print(referred_paper)
        if "article-title" in referred_paper.keys():
            return referred_paper["article-title"]
        elif "unstructured" in referred_paper.keys():
            if '“' in referred_paper["unstructured"]:
                # conference/journal paper
                return referred_paper["unstructured"].split('“')[1].split('”')[0]
            else:
                # book
                return ReferredPaper.find_article_title_book(referred_paper["unstructured"])
        elif "DOI" in referred_paper.keys():
            p =  get_paper_meta_through_doi(referred_paper["DOI"])
            if p:
                return get_paper_meta_through_doi(referred_paper["DOI"])["message"]["title"][0]
            else:
                return None
        return None

    @staticmethod
    def find_article_title_book(s: str):
        if "\n" in s:
            return s[:s.find(",")]
        elif ":" in s:
            return s[s.find(":")+1:s.find(".", s.find(":"))]
        else:
            comma = [i for i, v in enumerate(s) if v == ',']
            # print(f"article title for book:{s}")
            if len(comma)>2:
                return s[comma[-3] + 1:comma[-2]]
            return s


class Paper:
    def __init__(self, ID: str, doi: str = None):
        self.ID = ID
        self.doi = doi
        self.referred_papers = None

    def __str__(self):
        return f"ID: {self.ID}  doi:{self.doi}  " \
               f"referred papers: {[str(each) for each in self.referred_papers] if self.referred_papers is not None else None}"

    def set_referred_papers(self, referred_papers: List[ReferredPaper]):
        self.referred_papers = referred_papers


def get_bib_parser():
    custom_parser = BibTexParser()
    custom_parser.ignore_nonstandard_types = False
    return custom_parser


def get_source_paper(source_pattern) -> List[Paper]:
    bib_list = glob.glob(source_pattern)
    papers = list()
    for bib in bib_list:
        with open(bib, encoding="utf-8") as bibtex_file:
            for entry in bibtexparser.load(bibtex_file, get_bib_parser()).entries:
                papers.append(Paper(entry["ID"], entry.get("doi", None)))
    return papers


def get_paper_meta_through_doi(doi: str):
    api = "https://api.crossref.org/v1/works/"
    headers = {
        'User-Agent': 'MashiroCl 1.0',
        'mailto': '441016116@qq.com'  # This is another valid field
    }
    result = None
    response = requests.get(api + doi,headers=headers)

    if 'json' in response.headers.get('content-type') and  response.status_code!=404:
        # print(response.headers)
        result = response.json()
    return result


def append_referred_papers(paper: Paper):
    if paper.doi is None:
        return
    res = get_paper_meta_through_doi(paper.doi)
    if res is None:
        return
    res = res["message"]
    referred_papers = list()
    if "reference" in res.keys():
        for referred_paper in res["reference"]:
            # print(paper.doi)
            article_title = ReferredPaper.get_article_title(referred_paper)
            doi = ReferredPaper.get_doi(referred_paper)
            if article_title or doi:
                referred_papers.append(ReferredPaper(article_title, doi))
    paper.set_referred_papers(referred_papers)

def paper2csv(writer, paper:Paper):
    if paper.referred_papers:
        for each in paper.referred_papers:
            writer.writerow([paper.ID, each.article_title, each.doi])

if __name__ == "__main__":
    source_pattern = "/Users/leichen/Code/hackson/2022_salab/salab-bib/src/*.bib"
    papers = get_source_paper(source_pattern)
    csv_file = "csv/references.csv"
    t = [i*80 for i in range(int(len(papers)/80))]
    t.append(len(papers))
    with open(csv_file, mode="a",  encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in range(len(t)-1):
            sleep(3)
            for each in tqdm(papers[t[i]:t[i+1]]):
                append_referred_papers(each)
                paper2csv(writer, each)


