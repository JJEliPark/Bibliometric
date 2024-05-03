import pandas as pd
from pybliometrics.scopus import AffiliationRetrieval
from tqdm import tqdm

data = pd.read_csv("./data/ai_research_papers.csv")

data_exploded = data.assign(author_afids=data['author_afids'].str.split(';')).explode('author_afids')
afids = list(data_exploded['author_afids'].unique())


columns = ['afid', 'affiliation_name', 'org_type', 'city', 'state', 'country']
df = pd.DataFrame(columns=columns)

failed = []
i = 0
for afid in afids :
    try :
        aff = AffiliationRetrieval(afid)
        new_row = [afid, aff.affiliation_name, aff.org_type, aff.city, aff.state, aff.country]
        df = df.append(pd.Series(new_row, index=df.columns), ignore_index=True)
        print(f"# : {i}, Afid : {afid}, Done.")
    except :
        print(f"Afid Failed: {afid}")
        failed.append(afid)
        continue
    i+=1


df.to_csv("./data/ai_papers_affiliations.csv", index = False)
print(f"Failed Afids : {failed}")