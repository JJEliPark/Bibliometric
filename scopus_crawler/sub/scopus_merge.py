from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
import pandas as pd

best_papers = pd.read_csv("./data/best_scopus.csv")
best_papers['best_yn'] = 1
scopus_query = pd.read_csv("./data/best_scopus_whole_madequery.csv")
scopus_query['best_yn'] = 0
scopus_load = pd.read_csv("./data/best_scopus_whole.csv")
scopus_load['best_yn'] = 0

#whole_data = pd.concat([best_papers, scopus_load])
whole_data = pd.concat([best_papers, scopus_query])
whole_data = pd.concat([whole_data, scopus_load])
whole_data = whole_data.drop_duplicates(subset='eid')
whole_data['year'] = whole_data['coverDate'].str[:4]
whole_data = whole_data.loc[(whole_data['affiliation_country'].notna())& (whole_data['year'] >= '1996')]

print("전체 Paper 수 : ", len(whole_data))
whole_data.to_csv('../data/ai_research_papers.csv', index= False)