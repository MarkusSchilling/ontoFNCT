import pandas as pd
# Function to transform inputs to IRIs.
def to_iri(input):
    try:
        return input.iri
    except:
        pass
    return input

# Function to write the result of a SPARQL query into a (pandas) data frame.
def sparql_result_to_df(res):
    l = []
    for row in res:
        r = [ to_iri(item)  for item in row]
        l.append(r)
    return pd.DataFrame(l)