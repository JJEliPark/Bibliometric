import pandas as pd
from pybliometrics.scopus import AffiliationRetrieval
from pybliometrics.scopus import AuthorRetrieval
from tqdm import tqdm

pd.set_option('display.max_columns', None)
data = pd.read_csv("./data/ai_research_papers.csv")
data.at[222653, 'author_names'] = 'Dudík, Miroslav;Haghtalab, Nika;Luo, Haipeng;Schapire, Robert E.;Syrgkanis, Vasilis;Vaughan, Jennifer Wortman'
data_exploded = data.assign(author_afids=data['author_afids'].str.split(';'), author_ids=data['author_ids'].str.split(';'), author_names = data['author_names'].str.split(';'))
data_exploded = data_exploded.explode(['author_afids', 'author_names', 'author_ids'])
data_exploded['author_rank'] = data_exploded.groupby('eid').cumcount() + 1
data_exploded = data_exploded[['eid', 'year', 'origin_ref','author_count', 'author_names', 'author_ids', 'author_afids', 'author_rank', 'citedby_count']]

data_affil = pd.read_csv("./data/ai_papers_affiliations.csv")

data_fin = pd.merge(data_exploded, data_affil, how = 'left', left_on = 'author_afids', right_on = 'afid')

auth_ids = list(data_fin.loc[data_fin['afid'].isna()]['author_ids'].unique())
columns = ['author_ids','afid', 'affiliation_name', 'org_type', 'city', 'state', 'country']
df = pd.DataFrame(columns=columns)

fail = []
i = 0
for auth_id in tqdm(auth_ids) :
    try :
        au = AuthorRetrieval(int(auth_id))
        new_row =  [auth_id, au.affiliation_current[0][0], au.affiliation_current[0][5], None, au.affiliation_current[0][10],  au.affiliation_current[0][11], au.affiliation_current[0][8]]
        df = df.append(pd.Series(new_row, index=df.columns), ignore_index=True)
        print(f"# : {i}, auth_id : {auth_id}, Done.")
    except :
        print(f"auth_id Failed: {auth_id}")
        fail.append(auth_id)
    i+=1


df.to_csv("./data/ai_papers_affiliations_append.csv", index = False)
