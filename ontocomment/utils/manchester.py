from autontomment.utils.javabridge import load_owlapi
load_owlapi()

from org.semanticweb.owlapi.model import OWLOntologyManager, OWLClass, IRI
from uk.ac.manchester.cs.owl.owlapi import OWLAnnotationPropertyImpl
from org.semanticweb.owlapi.apibinding import OWLManager
from org.semanticweb.owlapi.io import StringDocumentSource, StringDocumentTarget
from org.semanticweb.owlapi.formats import ManchesterSyntaxDocumentFormat
from org.semanticweb.owlapi.manchestersyntax.renderer import ManchesterOWLSyntaxOWLObjectRendererImpl
from org.semanticweb.owlapi.util import AnnotationValueShortFormProvider 
from java.util import ArrayList, HashMap

from itertools import chain
from collections import defaultdict
from rdflib import Graph, URIRef

import re

def class_description(ontology: Graph, c: URIRef) -> str:
    """
    Convert an ontology to Manchester syntax.

    Args:
        ontology (Graph): Loaded ontology as a graph.
        c (URIRef): Class to be described using Manchester syntax.

    Returns:
        str: Output ontology as a string in Manchester Syntax.
    """
    manager = OWLManager.createOWLOntologyManager()
    ontology_str = ontology.serialize(format="xml")
    onto = manager.loadOntologyFromOntologyDocument(StringDocumentSource(ontology_str))

    renderer = ManchesterOWLSyntaxOWLObjectRendererImpl()
    label_property = OWLAnnotationPropertyImpl(IRI.create("http://www.w3.org/2000/01/rdf-schema#label"))
    
    properties = ArrayList([label_property])
    lang_map = HashMap()
    lang_map.put(label_property, ArrayList(["en"]))
    sfp = AnnotationValueShortFormProvider(properties, lang_map, manager)
    renderer.setShortFormProvider(sfp)
    
    iri = IRI.create(str(c))
    c = manager.getOWLDataFactory().getOWLClass(iri)

    desc = {
        "subclass of": ("SubClassOf", onto.getSubClassAxiomsForSubClass(c)),
        "equivalent to": ("EquivalentTo", onto.getEquivalentClassesAxioms(c)),
        "disjoint union of": ("DisjointUnionOf", onto.getDisjointUnionAxioms(c)),
        "disjoint with": ("DisjointWith", onto.getDisjointClassesAxioms(c)),
        "superclass of": ("SubClassOf", onto.getSubClassAxiomsForSuperClass(c)),
    }

    return {
        k: list(set([str(renderer.render(c).split(x)[-1].strip()) for c in y]))
        for k, (x, y) in desc.items()
    }

