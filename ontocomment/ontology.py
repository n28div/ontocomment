from typing import List, Union
import random
import rdflib

class Ontology(object):
  def __init__(self, ontology: str):
    self.graph = rdflib.Graph()
    self.graph.parse(ontology)

    # extract the set of classes in the ontology
    QUERY = """
      SELECT ?uri 
      WHERE { 
        { ?uri a owl:Class } UNION  { ?uri a rdfs:Class } .
        ?uri rdfs:comment ?comment . 
        FILTER (STRLEN(?comment) != 0)
      }
    """
    self._classes = [ row["uri"] for row in self.graph.query(QUERY) ]

  def sample_classes(self, k: int = 1) -> Union[rdflib.URIRef, List[rdflib.URIRef]]:
    """
    Sample a random class from the ontology graph.

    Args:
        k (int, optional): Number of elements to sample. Defaults to 1.

    Returns:
        Union[rdflib.URIRef, List[rdflib.URIRef]]: Sample element(s).
    """
    return random.choices(self._classes, k=k) if k > 1 else random.choice(self._classes)

  def negative_sample_classes(self, anchor: rdflib.URIRef, k: int = 1) -> Union[rdflib.URIRef, List[rdflib.URIRef]]:
    """
    Sample a random class from the ontology graph that is not anchor.

    Args:
        anchor (rdflib.URIRef: Element for which negative examples are drawn.
        k (int, optional): Number of elements to sample. Defaults to 1.

    Returns:
        Union[rdflib.URIRef, List[rdflib.URIRef]]: Sample element(s).
    """
    classes = list(set(self._classes).difference(anchor))
    return random.choices(classes, k=k) if k > 1 else random.choice(classes)