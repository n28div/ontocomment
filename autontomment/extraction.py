from typing import Dict
import rdflib
from itertools import chain
from collections import defaultdict
from autontomment.utils.manchester import class_description

def query_literal(graph: rdflib.Graph, query: str):
  rows = graph.query(query)
  try:
    res = next(iter(rows))
    return str(list(res.asdict().values())[0])
  except:
    return ""

def extract_label(graph: rdflib.Graph, uri: rdflib.URIRef):
  return query_literal(graph, """
  SELECT ?label
  WHERE {
    <%s> rdfs:label ?label .
    FILTER (LANG(?label) = "en") .
  }
  """ % str(uri))

def extract_comment(graph: rdflib.Graph, uri: rdflib.URIRef):
  return query_literal(graph, """
  SELECT ?comment
  WHERE {
    <%s> rdfs:comment ?comment .
  }
  """ % str(uri)).replace("\n", " ")

def extract_class_description(graph: rdflib.Graph, _class: rdflib.URIRef):
  return {
    "class_label": extract_label(graph, _class),
    "class_comment": extract_comment(graph, _class),
    "facts": class_description(graph, _class)
  }