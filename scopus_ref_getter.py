import pandas as pd
from pybliometrics.scopus import ScopusSearch

# Load data
data = pd.read_csv("./data/ai_research_papers.csv")
origin_eids = data['eid']
origin_eids_set = set(origin_eids)

columns = ['eid', 'eid_citedby_ai', 'citedby_count_ai', 'eid_citedby_etc', 'citedby_count_etc']

try:
    df = pd.read_csv('./data/ai_papers_citations.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=columns)

try:
    failed_eids = pd.read_csv('./data/failed_eids.csv')['eid'].tolist()
except FileNotFoundError:
    failed_eids = []  # List to store failed eids

# Find the index of the last failed eid if it exists
start_index = 0
if failed_eids:
    last_failed_eid = failed_eids[-1]
    start_index = data[data['eid'] == last_failed_eid].index[0]

print(f"start from # : {start_index}, Eid : {last_failed_eid}")

# Process each row starting from the row after the last failed eid
for i, row in enumerate(data.iloc[start_index:].itertuples(), start_index):
    e = row.eid

    if row.citedby_count == 0:
        continue

    q = f"REF({e})"
    try:
        s = ScopusSearch(q, verbose=False, download=True)
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
        break  # Stops the loop at the first failure

# Save DataFrame to CSV
df.to_csv("./data/ai_papers_citations.csv", index=False)

# Save failed eids to a CSV file
if failed_eids:
    pd.DataFrame(failed_eids, columns=['eid']).to_csv('./data/failed_eids.csv', index=False)
