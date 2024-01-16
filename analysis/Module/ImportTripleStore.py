### read in dataframe
import owlready2 as or2
from Module import Functions as f
# For exemplary reasons, OWLready2 is used to create a local triple store to perform queries
#triple_store = or2.World(filename="triple_store.sqlite3")

# Load the required ontologies: Owlready2 doesn't follow the redirects from https://w3id.org/...
# We provide the download links for the ontologies directly.
# https://owlready2.readthedocs.io/en/latest/onto.html?highlight=rdf%20xml#loading-an-ontology-from-owl-files
def get_triple_store(link_core, link_ontoFNCT, link_data):
    triple_store = or2.World()
    triple_store.get_ontology(link_core).load() # https://w3id.org/pmd/co
    triple_store.get_ontology(link_ontoFNCT).load()  # https://w3id.org/ontofnct
    # triple_store.get_ontology("file://ontology.rdf").load()  # Local file import of OntoFNCT
    triple_store.get_ontology(link_data).load()  # Examplary data mapped file on GitHub (https://github.com/MarkusSchilling/ontoFNCT/ontoFNCT_exemplary_data_mapping.rdf)
    # triple_store.get_ontology("file://ontoFNCT_exemplary_data_PE-HD.rdf").load()  # Local file import to triple store
    return triple_store

# "https://raw.githubusercontent.com/MarkusSchilling/ontoFNCT/main/analysis/ontoFNCT_exemplary_data_PE-HD.rdf"
# Query for the number of instances of type "FNCT" in the dataset (number of FNCT tests included)
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
    ?s a pmdco:TestPiece .
    ?p pmdco:input ?s .
    ?s pmdco:characteristic ?materialDesc .
    ?materialDesc a pmdco:materialDesignation .
    ?materialDesc pmdco:value ?material .
    ?p pmdco:characteristic ?mediumInst .
    ?mediumInst a pmdco:Medium .
    ?mediumInst pmdco:value ?medium .
    ?p pmdco:output ?tfInst .
    ?tfInst a ontoFNCT:TimeToFailure .
    ?tfInst pmdco:value ?timeToFailure .
    ?p pmdco:output ?stressInst .
    ?stressInst a ontoFNCT:NominalTensileStress .
    ?stressInst pmdco:value ?stressMeasured .
    } ORDER BY ?material ?medium ?stressMeasured
    """
    )
    # Create dataframe comprising the result of the SPARQL query. This may take some time depending on the complexity of the query.
    res = triple_store.sparql(query)
    data = f.sparql_result_to_df(res)
    return data
    