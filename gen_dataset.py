import argparse
from ontocomment.ontology import Ontology
from ontocomment.extraction import extract_class_description
from datasets import Dataset

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="The ontology that is being used as example.")
parser.add_argument("-s", "--size", required=True, type=int, help="Number of experiments extracted from the ontology.")
parser.add_argument("-e", "--examples", default=3, type=int, required=True, help="Number of examples for each prompt.")
parser.add_argument("-o", "--output", required=True, help="Output path for the dataset.")

if __name__ == "__main__":
  args = parser.parse_args()
  onto = Ontology(args.input)

  # generate dataset
  def gen_data(num: int, examples: int = 3):
    for _ in range(num):
      target = onto.sample_classes(k=1)
      target_desc = extract_class_description(onto.graph, target)

      refs = onto.negative_sample_classes(target, k=examples)
      refs_desc = [ extract_class_description(onto.graph, d) for d in refs ]

      yield {
        "target": target,
        "target_description": target_desc,
        "references": refs,
        "references_description": refs_desc
      }
  
  dataset = Dataset.from_generator(gen_data, gen_kwargs={"num": args.size, "examples": args.examples})
  dataset.save_to_disk(args.output)

  