import argparse
from datasets import Dataset
import jinja2
import json
from tqdm.auto import tqdm
import os
from datetime import datetime
import re

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", required=True, help="The dataset used for the experiments.")
parser.add_argument("-o", "--output", help="Directory where JSON will be saved.")

if __name__ == "__main__":
  args = parser.parse_args()

  dataset = Dataset.load_from_disk(args.dataset)

  # load prompts
  environment = jinja2.Environment(loader=jinja2.FileSystemLoader("prompts/"))
  template = environment.get_template("baseline")

  results = []
  for sample in (pbar := tqdm(dataset)):
    prompt = template.render(
      target=sample["target_description"], 
      references=sample["references_description"])

    output = re.sub("\s+", " ", prompt.strip().replace("\n", " ")).replace(", .", ".")

    results.append({
      "data": sample,
      "output": output,
    })

  output = {
    "args": vars(args),
    "results": results
  }
  
  now = datetime.now()
  filename = now.strftime("%y-%m-%d_%H%M%S%f")
  with open(os.path.join(args.output, f"{filename}.json"), "w") as f:
    json.dump(output, f)
