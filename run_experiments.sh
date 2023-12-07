#!/bin/bash

for model in "tiiuae/falcon-7b-instruct" "meta-llama/Llama-2-7b-chat-hf" "Intel/neural-chat-7b-v3-1"
do
  for dataset in "datasets/arco_100_3/" "datasets/dbpedia_100_3/" "datasets/dul_100_3/" "datasets/frbr_100_3/" "datasets/helis_100_3/" "datasets/schemaorg_100_3/" "datasets/foodon_100_3/" "datasets/go_100_3/" 
  do
    for prompt in "prompt_0" "prompt_0_role" "prompt_1" "prompt_1_role" "prompt_2" "prompt_2_role" "prompt_3" "prompt_3_role" "prompt_4" "prompt_4_role"
    do
      python experiments.py -d $dataset -t $prompt -o output/ -m $model --max-length 150 -o output/
    done
  done
done
