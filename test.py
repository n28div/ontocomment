import jinja2
import rdflib
from autontomment.extraction import extract_class_description

g = rdflib.Graph()
g.parse("/home/n28div/university/phd/llm_comment_ontology/ontology/DUL.owl")
#g.parse("http://www.w3.org/2000/01/rdf-schema")
DUL = rdflib.Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")

environment = jinja2.Environment(loader=jinja2.FileSystemLoader("prompts/"))
template = environment.get_template("prompt_1.txt")
descriptions = [
  extract_class_description(g, DUL.Transition),
  extract_class_description(g, DUL.Person)
]

target = extract_class_description(g, DUL.Object)

rendered_template = template.render(descriptions=descriptions, target=target)
rendered_template = rendered_template.replace("\n\n", "\n").strip()

print(rendered_template)