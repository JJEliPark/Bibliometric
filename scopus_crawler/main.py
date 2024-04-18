import pandas as pd
from sub.scopus_load_all import ScopusCrawlerAll
from sub.scopus_load_all_madequery import ScopusCrawlerQuery
from sub.scopus_load import ScopusCrawlerBest
from sub.best_paper_awards_crawl import BestPaperAwardsCrawler
from pybliometrics.scopus.utils import config
import argparse


def main():
    
    api_key = config['Authentication']['APIKey']
    if len(api_key) == 0 :
        print("There's no default key for SCOPUS API")
        api_key = input("Please enter your API key: ")


    # 스크립트 순서대로 실행
    awards_crawler = BestPaperAwardsCrawler()
    awards_crawler.run()
    print("*******best_paper_awards_crawl.csv Created.")

    awards_scopus_crawler = ScopusCrawlerBest(api_key=api_key)
    awards_scopus_crawler.search_papers()
    print("*******best_paper_awards_scopus.csv Created.")

    # ScopusQueryExecutor 클래스 인스턴스화 및 실행
    query_executor = ScopusCrawlerQuery(api_key=api_key)
    query_executor.run_queries()
    print("*******best_scopus_predefined.csv Created.")

    # ScopusPaperSearch 클래스 인스턴스화 및 실행
    all_searcher = ScopusCrawlerAll(api_key=api_key)
    all_searcher.run_search()
    print("*******best_scopus_whole.csv Created.")

    # BestPaperAwardsCrawler 클래스 인스턴스화 및 실행

if __name__ == "__main__":
    main()
    best_papers = pd.read_csv("./sub_data/best_paper_awards_scopus.csv")
    best_papers['best_yn'] = 1
    scopus_query = pd.read_csv("./sub_data/best_scopus_predefined.csv")
    scopus_query['best_yn'] = 0
    scopus_load = pd.read_csv("./sub_data/best_scopus_whole.csv")
    scopus_load['best_yn'] = 0

    #whole_data = pd.concat([best_papers, scopus_load])
    whole_data = pd.concat([best_papers, scopus_query])
    whole_data = pd.concat([whole_data, scopus_load])
    whole_data = whole_data.drop_duplicates(subset='eid')
    whole_data['year'] = whole_data['coverDate'].str[:4]
    whole_data = whole_data.loc[(whole_data['affiliation_country'].notna())& (whole_data['year'] >= '1996')]

    print("전체 Paper 수 : ", len(whole_data))
    whole_data.to_csv('../data/ai_research_papers.csv', index= False)
