import argparse
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList
import evaluate
import jinja2
import json
from tqdm.auto import tqdm
import os
from datetime import datetime

class FullComment(StoppingCriteria):
  """
  FullComment class stops generating text when a newline is added 
  i.e. when the comment has been fully filled.
  """
  def __init__(self, tokenizer):
    self.tokenizer = tokenizer

  def __call__(self, input_ids, scores):
    decoded = self.tokenizer.decode(input_ids[0])
    return decoded.endswith("\n")


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", required=True, help="The dataset used for the experiments.")
parser.add_argument("-m", "--model", default="tiiuae/falcon-7b-instruct", help="HuggingFace model path.")
parser.add_argument("-t", "--template", required=True, help="Prompting template from prompts/ directory.")
parser.add_argument("--max-length", default=50, help="Maximum length of the comment.")
parser.add_argument("-o", "--output", help="Directory where JSON will be saved.")

if __name__ == "__main__":
  args = parser.parse_args()

  dataset = Dataset.load_from_disk(args.dataset)

  # load prompts
  environment = jinja2.Environment(loader=jinja2.FileSystemLoader("prompts/"))
  template = environment.get_template(args.template)

  results = []
  for sample in (pbar := tqdm(dataset)):
    prompt = template.render(
      target=sample["target_description"], 
      references=sample["references_description"])#.replace("\n\n", "\n")
    print(prompt)
    break