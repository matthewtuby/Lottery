#!/bin/sh

# run pylint on everything
python3 -m pylint main.py > ./analysis/pylint_main.txt
python3 -m pylint lottery.py > ./analysis/pylint_lottery.txt
python3 -m pylint lotto_test.py > ./analysis/pylint_lotto_test.txt

# run mypy on everyhint
python3 -m mypy main.py > ./analysis/pylint_main.txt
python3 -m mypy lottery.py > ./analysis/pylint_lottery.txt
python3 -m mypy lotto_test.py > ./analysis/pylint_lotto_test.txt

# run tests
python3 lotto_test.py > tests.txt
