### read in dataframe
import owlready2 as or2
from Module import Functions as f
# To show the general procedure as an example, OWLready2 is used to create a local triple store to perform queries

# Load the required ontologies that are directly provided by the download links for the ontologies (hosted on GitHub).
# More information: https://owlready2.readthedocs.io/en/latest/onto.html?highlight=rdf%20xml#loading-an-ontology-from-owl-files
def get_triple_store(link_core, link_ontoFNCT, link_data):
    triple_store = or2.World()
    triple_store.get_ontology(link_core).load() # https://w3id.org/pmd/co
    triple_store.get_ontology(link_ontoFNCT).load()  # https://w3id.org/ontofnct
    triple_store.get_ontology(link_data).load()  # Example data mapped file on GitHub (https://github.com/MarkusSchilling/ontoFNCT/ontoFNCT_exemplary_data_mapping.rdf)
    return triple_store

# "https://raw.githubusercontent.com/MarkusSchilling/ontoFNCT/main/analysis/ontoFNCT_exemplary_data_PE-HD.rdf"
# Query to obtain material names, media measured in and the FNCT results considering time to failure and the measured stress
def get_dataframe(triple_store):
    query=("""
    PREFIX pmdco: <https://w3id.org/pmd/co/>
    PREFIX ontoFNCT: <https://w3id.org/ontofnct/>

    SELECT DISTINCT ?processID ?material ?medium ?timeToFailure ?stressMeasured
    WHERE {
    ?p a ontoFNCT:FullNotchCreepTest .
    ?p pmdco:characteristic ?processIDInst .
    ?processIDInst a pmdco:ProcessIdentifier .
    ?processIDInst pmdco:value ?processID .
    ?s a pmdco:Specimen .
    ?p pmdco:input ?s .
    ?s pmdco:characteristic ?materialDesc .
    ?materialDesc a pmdco:materialDesignation .
    ?materialDesc pmdco:value ?material .
    ?p pmdco:participant ?mediumInst .
    ?mediumInst a pmdco:Medium .
    ?mediumInst pmdco:value ?medium .
    ?p pmdco:output ?tfInst .
    ?tfInst a ontoFNCT:TimeToFailure .
    ?tfInst pmdco:value ?timeToFailure .
    ?p pmdco:output ?stressInst .
    ?stressInst a ontoFNCT:MeasuredTensileStress .
    ?stressInst pmdco:value ?stressMeasured .
    } ORDER BY ?material ?medium ?stressMeasured
    """
    )
    # Create dataframe comprising the result of the SPARQL query. This may take some time depending on the complexity of the query.
    res = triple_store.sparql(query)
    data = f.sparql_result_to_df(res)
    return data
    