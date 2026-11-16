# Lab 6 — Laundry Service Coverage

Source: SETAPESU26/L6_L7_41_laundry_service, Lab 6.

Run from this folder:

```bash
python -m pip install pytest coverage
python -m coverage run --branch --source=laundry_service -m pytest -q
python -m coverage report -m
```

The initial 12 tests reached 94% combined coverage with 36/37 statements and 23/26 branches covered.
Adding `test_heavy_standard_charge` and `test_dropoff_late` reached 100% statement and branch coverage with 14 passing tests.

For the required two commits, first commit the module and test file without those final two test functions, plus a screenshot of the initial report. Then add the two tests, rerun coverage, capture the final report, and make the second commit.
