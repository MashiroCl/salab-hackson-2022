import unittest
from extractor import ReferredPaper, get_source_paper, append_referred_papers

class MyTestCase(unittest.TestCase):
    def test_get_article_title_conference_paper(self):
        d = {"key": "1",
             "doi-asserted-by": "crossref",
             "unstructured": "[1] N. Sae-Lim, S. Hayashi, and M. Saeki, “Toward proactive refactoring: An exploratory study on decaying modules,” Proc. third International Workshop on Refactoring (IWOR&apos;19), pp.1-10, 2019. 10.1109/iwor.2019.00015",
             "DOI": "10.1109/IWoR.2019.00015"
             }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual("Toward proactive refactoring: An exploratory study on decaying modules,",res)

    def test_find_article_title_book(self):
        s = "M. Fowler, Refactoring: Improving the Design of Existing Code, Addison-Wesley, 1999."
        res = ReferredPaper.find_article_title_book(s)
        self.assertEqual(" Refactoring: Improving the Design of Existing Code", res)

    def test_get_article_title_book(self):
        d = {
            "key": "3",
            "unstructured": "[3] M. Fowler, Refactoring: Improving the Design of Existing Code, Addison-Wesley, 1999."
            }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual(" Refactoring: Improving the Design of Existing Code",res)

    def test_get_article_title_book2(self):
        d = {
                "key": "52_CR1",
                "unstructured": "OMG: Model-Driven Architecture, \n                    \n                      http://www.omg.org/mda/"
            }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual("OMG: Model-Driven Architecture",res)

    def test_get_article_title_book3(self):
        d = {
                "key": "52_CR6",
                "unstructured": "Chabarek, F.: Development of an OCL-parser for UML-extensions. Master’s thesis, Technical University of Berlin (2004)"
                }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual(" Development of an OCL-parser for UML-extensions",res)

    def test_get_article_title_doi(self):
        d= {
            "key": "ref11",
            "doi-asserted-by": "publisher",
            "DOI": "10.1109/CSMR.2008.4493315"
            }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual("Extracting Domain Ontologies from Domain Specific APIs",res)

    def test_get_article_title_article_title(self):
        d= {
            "key": "ref1",
            "first-page": "249",
            "article-title": "Goal-oriented requirements engineering: A guided tour",
            "author": "van lamsweerde",
            "year": "2001",
            "journal-title": "Proc 5th International Symposium on Requirements Engineering"
            }
        res = ReferredPaper.get_article_title(d)
        self.assertEqual("Goal-oriented requirements engineering: A guided tour",res)

    def test_append_referred_papers(self):
        source_pattern = "/Users/leichen/Code/hackson/2022_salab/salab-bib/src/*.bib"
        papers = get_source_paper(source_pattern)
        for each in papers:
            append_referred_papers(each)

if __name__ == '__main__':
    unittest.main()
