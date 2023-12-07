#!/bin/bash

for dataset in "datasets/arco_100_3/" "datasets/dbpedia_100_3/" "datasets/dul_100_3/" "datasets/frbr_100_3/" "datasets/helis_100_3/" "datasets/schemaorg_100_3/" "datasets/foodon_100_3/" "datasets/go_100_3/" 
do
    python baseline.py -d $dataset -o baseline_output/
done

