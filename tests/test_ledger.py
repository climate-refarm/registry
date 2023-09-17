import json
import pandas as pd
import glob

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.utils.paths import ledger_folder, projects_folder
from helpers.models.summary import ClimateOffsetPortfolioSummary
import helpers.validation.checks as checks


def test_main_ledger_exists():
  assert(os.path.exists(ledger_folder("main.csv")))


def test_climate_offset_portfolio_summary_exists():
  path = ledger_folder("climate_offset_portfolio/summary.json")
  assert(os.path.exists(path))
  with open(path, "r") as f:
    ClimateOffsetPortfolioSummary.model_validate(json.load(f))


def test_check_serial_numbers_are_unique():
  df = pd.read_csv(ledger_folder("main.csv"))
  checks.check_serial_numbers_are_unique(df)


def test_check_credits_match_model():
  df = pd.read_csv(ledger_folder("main.csv"))
  checks.check_credits_match_model(df)
