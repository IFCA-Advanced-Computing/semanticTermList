import urllib
import rdflib
import rdflib_jsonld
import sys
#v1 import nltk, re, pprint
import os
from nltk import word_tokenize
import argparse

parser=argparse.ArgumentParser(
    description='''List of terms included in a document from a RDF schema ''',
    epilog="""By INDIGO-DataCloud (IFCA-CSIC)""")
parser.add_argument('--rdf', type=str, default='http://smw-rda.esc.rzg.mpg.de/exports/tedt.rdf', help='Link to RDF URL where the list of terms is',required=True)
parser.add_argument('--doc', type=str, default='doc.txt', help='Route to path where the document is. Expected type: .txt',required=True)
args=parser.parse_args()

def get_terms(graph):
    print ("Lista terms")
    predicate_query = graph.query("""
                     PREFIX tedt: <http://smw-rda.esc.rzg.mpg.de/>
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     select ?name
                     where {?s rdf:_1 ?name}
                     """)
    return predicate_query
 
def get_description(graph,term):
    predicate_query = graph.query("""
                     PREFIX tedt: <http://smw-rda.esc.rzg.mpg.de/>
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     select ?desc
                     where {?a rdf:_1 ?name . FILTER (str(?name) = "%s") .
                            ?a tedt:text ?desc
                            }
                     """ % term)

    for row in predicate_query:
        print('%s' % row)
        break

def get_reference(graph,term):
    predicate_query = graph.query("""
                     PREFIX tedt: <http://smw-rda.esc.rzg.mpg.de/>
                     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                     select ?desc
                     where {?a rdf:_1 ?name . FILTER (str(?name) = "%s") .
                            ?a tedt:reference ?desc
                            }
                     """ % term)


    # For each results print the value
    for row in predicate_query:
        print('%s' % row)
        break


def main(argv = sys.argv):
    
    # Code from Fetching Data and Parsing Data examples (Term List)
    #uri = 'http://smw-rda.esc.rzg.mpg.de/exports/tedt.rdf'
    uri = args.rdf
    request_headers = {'Accept': 'application/rdf+xml'}
    request = urllib.request.Request(uri, headers = request_headers)
    response = urllib.request.urlopen(request).read()
    graph = rdflib.Graph()
    graph.parse(data=response, format='xml')

#v1    #Preparing the document for being analyzed
#v1    f=open('doc.txt','rU')
#v1    raw=f.read()
#v1    tokens = nltk.word_tokenize(raw)
#v1    text = nltk.Text(tokens)
    
    term_list = get_terms(graph)

#v1    for row in term_list:
#v1        if text.count("%s".replace("_"," ") % row) > 0:
#v1            print ("Term: %s".replace("_"," ") % row)
#v1            print ("Description:")
#v1            get_description(graph,"%s" % row)
#v1            print ("\n")
#v1            print ("Reference: \n")
#v1            get_reference(graph,"%s" % row)
#v1           print ("\n")

    #path = "doc.txt"
    path = args.doc
    with open(os.path.join('',path), 'r') as myfile:
        data=myfile.read().replace('\n', '')
    data = data.lower()
    for row in term_list:
        if data.find(("%s" % row).lower().replace("_"," "))>=0:
            print ("Term: %s".replace("_"," ") % row)
            print ("Description:")
            get_description(graph,"%s" % row)
            print ("\n")
            print ("Reference: \n")
            get_reference(graph,"%s" % row)
            print ("\n")
    #get_terms(graph)
    #get_description(graph,'Metadata')

if __name__ == "__main__":
    main()
