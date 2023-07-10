from typing import Dict
import rdflib
from itertools import chain
from collections import defaultdict
from autontomment.utils.manchester import class_description

def query_literal(graph: rdflib.Graph, query: str) -> str:
  """
  Query for a single literal using SPARQL.

  Args:
      graph (rdflib.Graph): Queried graph.
      query (str): Query to run.

  Returns:
      str: Litaral extracted.
  """
  rows = graph.query(query)
  try:
    res = next(iter(rows))
    return str(list(res.asdict().values())[0])
  except:
    return ""

def extract_label(graph: rdflib.Graph, uri: rdflib.URIRef) -> str:
  """
  Extract the label of a URI from the graph.

  Args:
      graph (rdflib.Graph): Ontology graph.
      uri (rdflib.URIRef): URI to extract label of.

  Returns:
      str: Extracted label
  """  
  return query_literal(graph, """
  SELECT ?label
  WHERE {
    <%s> rdfs:label ?label .
    FILTER (LANG(?label) = "en") .
  }
  """ % str(uri))

def extract_comment(graph: rdflib.Graph, uri: rdflib.URIRef) -> str:
  """
  Extract the comment of a URI from the graph.

  Args:
      graph (rdflib.Graph): Ontology graph.
      uri (rdflib.URIRef): URI to extract comment of.

  Returns:
      str: Extracted comment
  """  
  return query_literal(graph, """
  SELECT ?comment
  WHERE {
    <%s> rdfs:comment ?comment . 
    FILTER(LANG(?comment) = "" || LANGMATCHES(LANG(?comment), "en"))
  }
  """ % str(uri)).replace("\n", " ")


def extract_is_domain_of(graph: rdflib.Graph, uri: rdflib.URIRef) -> str:
  """
  Extract the labels of the predicates of which a URI is domain of.

  Args:
      graph (rdflib.Graph): Ontology graph.
      uri (rdflib.URIRef): Reference URI.

  Returns:
      str: Extracted label
  """  
  query = """
  SELECT ?label ?range
  WHERE {
    [] rdfs:domain <%s> ;
       rdfs:range [ rdfs:label ?range ] ;
       rdfs:label ?label .
    FILTER (LANG(?label) = "en") .
    FILTER (LANG(?range) = "en") .
  }
  """ % str(uri)

  rows = graph.query(query)
  labels = [f"{row['label']} a {row['range']}" for row in rows]
  return labels

def extract_is_range_of(graph: rdflib.Graph, uri: rdflib.URIRef) -> str:
  """
  Extract the labels of the predicates of which a URI is range of.

  Args:
      graph (rdflib.Graph): Ontology graph.
      uri (rdflib.URIRef): Reference URI.

  Returns:
      str: Extracted label
  """  
  query = """
  SELECT ?label ?domain
  WHERE {
    [] rdfs:range <%s> ;
       rdfs:domain [ rdfs:label ?domain ] ;
       rdfs:label ?label .
    FILTER (LANG(?label) = "en") .
    FILTER (LANG(?domain) = "en") .
  }
  """ % str(uri)

  rows = graph.query(query)
  labels = [f"{row['domain']} {row['label']}" for row in rows]
  return labels

def extract_class_description(graph: rdflib.Graph, _class: rdflib.URIRef) -> Dict:
  """
  Extract the description of a class from the graph. 

  Args:
      graph (rdflib.Graph): Ontology graph.
      _class (rdflib.URIRef): Class that will be described.

  Returns:
      Dict[str]: Description of the class with three keys: 
      - label
      - comment
      - facts which contains the set of axioms of the class 
        (subClass, equivalence, superclass) expressed
        using Manchester syntax.
  """
  return {
    "label": extract_label(graph, _class),
    "comment": extract_comment(graph, _class),
    "facts": {
      **class_description(graph, _class),
      "is domain of": extract_is_domain_of(graph, _class),
      "is range of": extract_is_range_of(graph, _class)
    }
  }