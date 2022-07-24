#!/bin/sh

# run pylint on everything
python3 -m pylint main.py > ./analysis/pylint_main.txt 2>&1
python3 -m pylint lottery.py > ./analysis/pylint_lottery.txt 2>&1
python3 -m pylint lotto_test.py > ./analysis/pylint_lotto_test.txt 2>&1

# run mypy on everyhing
python3 -m mypy main.py > ./analysis/mypy_main.txt 2>&1
python3 -m mypy lottery.py > ./analysis/mypy_lottery.txt 2>&1
python3 -m mypy lotto_test.py > ./analysis/mypy_lotto_test.txt 2>&1

# run bandit
python3 -m bandit main.py > ./analysis/bandit_main.txt 2>&1
python3 -m bandit lottery.py > ./analysis/bandit_lottery.txt 2>&1
python3 -m bandit lotto_test.py > ./analysis/bandit_lotto_test.txt 2>&1

# run tests
python3 lotto_test.py > ./analysis/tests.txt 2>&1
