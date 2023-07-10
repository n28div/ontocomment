#!/bin/bash

python experiments.py -d datasets/arco_100_3/ -t prompt_1 -o output/
python experiments.py -d datasets/arco_100_3/ -t prompt_2 -o output/
python experiments.py -d datasets/arco_100_3/ -t prompt_3 -o output/
python experiments.py -d datasets/arco_100_3/ -t prompt_4 -o output/

python experiments.py -d datasets/arco_100_3/ -t prompt_1 -o output/ --max-length 100
python experiments.py -d datasets/arco_100_3/ -t prompt_2 -o output/ --max-length 100
python experiments.py -d datasets/arco_100_3/ -t prompt_3 -o output/ --max-length 100
python experiments.py -d datasets/arco_100_3/ -t prompt_4 -o output/ --max-length 100

python experiments.py -d datasets/arco_100_3/ -t prompt_1 -o output/ --max-length 150
python experiments.py -d datasets/arco_100_3/ -t prompt_2 -o output/ --max-length 150
python experiments.py -d datasets/arco_100_3/ -t prompt_3 -o output/ --max-length 150
python experiments.py -d datasets/arco_100_3/ -t prompt_4 -o output/ --max-length 150
