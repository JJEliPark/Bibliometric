import pandas as pd
from pybliometrics.scopus import ScopusSearch

# Load data
data = pd.read_csv("./data/ai_research_papers.csv")
origin_eids = data['eid']
origin_eids_set = set(origin_eids)

columns = ['eid', 'eid_citedby_ai', 'citedby_count_ai', 'eid_citedby_etc', 'citedby_count_etc']
df = pd.DataFrame(columns=columns)

failed_eids = []  # List to store failed eids

# Process each row
for i, row in enumerate(data.itertuples(), 1):
    e = row.eid
    if row.citedby_count == 0:
        continue

    q = f"REF({e})"
    try:
        s = ScopusSearch(q, verbose=False)
        ref_by = set(s.get_eids())
        in_origin = list(origin_eids_set.intersection(ref_by))
        in_origin_n = len(in_origin)
        in_origin = ';'.join(in_origin)
        not_origin = ref_by - origin_eids_set
        not_origin = list(not_origin)
        not_origin_n = len(not_origin)
        not_origin = ';'.join(not_origin)
        new_row = [e, in_origin, in_origin_n, not_origin, not_origin_n]
        df = df.append(pd.Series(new_row, index=df.columns), ignore_index=True)
        print(f"# : {i}, Eid : {e}, Done.")
    except Exception as ex:
        print(f"{e} Failed: {str(ex)}")
        failed_eids.append(e)
        break

# Save DataFrame to CSV
df.to_csv("./data/ai_papers_citations.csv")

# Save failed eids to a CSV file
if failed_eids:
    pd.DataFrame(failed_eids, columns=['eid']).to_csv('./data/failed_eids.csv')
