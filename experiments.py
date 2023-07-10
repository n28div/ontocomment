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
    return decoded.endswith(".\n")

rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")
chrf = evaluate.load("chrf")
meteor = evaluate.load("meteor")


def compute_metrics(pred, true):
  pred = [pred]
  refs = [true]

  bert_score = bertscore.compute(predictions=pred, references=refs, lang="en")
  return {
    **rouge.compute(predictions=pred, references=refs),
    **meteor.compute(predictions=pred, references=refs),
    "bertscore_precision": bert_score["precision"][0],
    "bertscore_recall": bert_score["recall"][0],
    "bertscore_f1": bert_score["f1"][0],
    "chrf": chrf.compute(predictions=pred, references=refs)["score"],
    "chrf+": chrf.compute(predictions=pred, references=refs, word_order=1)["score"],
    "chrf++": chrf.compute(predictions=pred, references=refs, word_order=2)["score"],
  }

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", required=True, help="The dataset used for the experiments.")
parser.add_argument("-m", "--model", default="tiiuae/falcon-7b-instruct", help="HuggingFace model path.")
parser.add_argument("-t", "--template", required=True, help="Prompting template from prompts/ directory.")
parser.add_argument("--max-length", default=50, type=int, help="Maximum length of the comment.")
parser.add_argument("-o", "--output", help="Directory where JSON will be saved.")

if __name__ == "__main__":
  args = parser.parse_args()

  dataset = Dataset.load_from_disk(args.dataset)

  tokenizer = AutoTokenizer.from_pretrained(args.model)
  tokenizer.pad_token_id = tokenizer.eos_token_id
  model = AutoModelForCausalLM.from_pretrained(
      args.model,
      trust_remote_code=True,
      device_map=0,
      load_in_8bit=True
  )

  # load prompts
  environment = jinja2.Environment(loader=jinja2.FileSystemLoader("prompts/"))
  template = environment.get_template(args.template)

  results = []
  for sample in (pbar := tqdm(dataset)):
    prompt = template.render(
      target=sample["target_description"], 
      references=sample["references_description"]).replace("\n\n", "\n")

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
  
    outputs = model.generate(
      input_ids=inputs["input_ids"],
      attention_mask=inputs["attention_mask"],
      max_new_tokens=args.max_length,
      num_return_sequences=1,
      return_dict_in_generate=True,
      pad_token_id=tokenizer.eos_token_id,
      stopping_criteria=StoppingCriteriaList([FullComment(tokenizer)])
    )

    prompt_length = len(inputs["input_ids"][0])
    new_text_ids = outputs.sequences[0][prompt_length:]
    output = tokenizer.decode(new_text_ids).strip()

    results.append({
      "data": sample,
      "output": output,
      "metrics": compute_metrics(output, sample["target_description"]["comment"])
    })

  output = {
    "args": vars(args),
    "results": results
  }
  
  now = datetime.now()
  filename = now.strftime("%y-%m-%d_%H%M")
  with open(os.path.join(args.output, f"{filename}.json"), "w") as f:
    json.dump(output, f)
