import json
import pandas as pd
import glob

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.utils.paths import ledger_folder, projects_folder
from helpers.models.summary import ClimateOffsetPortfolioSummary
import helpers.validation.checks as checks


def test_check_all_projects_have_monitoring():
  checks.check_all_projects_have_monitoring()


def test_check_all_projects_have_docs():
  checks.check_all_projects_have_docs()
