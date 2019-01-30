#!/usr/bin/env bash
$WD =  "C:/Users/tyler/PycharmProjects/untitled/"
rm /test_results/*
touch $WD/test_results/8bits100trials.txt
touch $WD/test_results/10bits100trials.txt
touch $WD/test_results/16bits100trials.txt
touch $WD/test_results/20bits100trials.txt
python HashAttack.py 100 8 > $WD/test_results/8bits100trials.txt
python HashAttack.py 100 10 > $WD/test_results/10bits100trials.txt
python HashAttack.py 100 16 > $WD/test_results/16bits100trials.txt
python HashAttack.py 100 20 > $WD/test_results/20bits100trials.txt