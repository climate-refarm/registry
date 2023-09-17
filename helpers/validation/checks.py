import pandas as pd

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import Credit, CreditStatus
from helpers.utils.paths import projects_folder


MINIMAL_MONITORING_COLUMNS = [
  "period",
  "total_credits_issued",
  "total_emission_reductions_tons_co2",
]


# Monitoring data can only include columns in this list. Columns outside of the
# list are either new co-benefits which should be included, or potential naming
# errors that should be corrected.
ALLOWED_MONITORING_COLUMNS = [
  "period",
  "total_credits_issued",
  "total_emission_reductions_tons_co2",
  "total_land_use_reduced_ha",
  "total_land_restored_ha",
  "total_land_conserved_ha",
  "total_animal_lives_saved",
  "total_meals_impacted"
]


def check_serial_numbers_are_unique(df: pd.DataFrame):
  """Check that serial numbers are unique."""
  if "serial_number" not in df.columns:
    df = df.copy().reset_index()

  if df.index.has_duplicates:
    print(df[df.duplicated()])
    raise ValueError("The credit serial numbers are not unique.")


def check_credits_match_model(df: pd.DataFrame):
  """Check that all credits are valid with respect to their Pydantic model."""
  _df = df.copy().reset_index()
  for i in range(len(_df)):
    row = _df.iloc[i]

    # Ensure the the credit schema is valid.
    Credit.model_validate(row.to_dict())


def check_all_serial_numbers_in_ledger(df_ledger: pd.DataFrame, serial_numbers: list[str]):
  """Ensure that all serial numbers exist in the ledger."""
  df = df_ledger.loc[serial_numbers].copy()
  if len(df) != len(serial_numbers):
    for sn in serial_numbers:
      if sn not in df:
        print(sn)
    raise ValueError("Some serial numbers are missing from the ledger")


def check_all_serial_numbers_retired(df_ledger: pd.DataFrame, serial_numbers: list[str]):
  """Ensure that all serial numbers in the list are retired."""
  df = df_ledger.loc[serial_numbers].copy().reset_index()
  not_retired = df[~df.status.isin([CreditStatus.retired, CreditStatus.pre_retired])]
  if len(not_retired) > 0:
    print(not_retired.index)
    raise ValueError("Found serial numbers that were not retired")


def check_all_projects_have_docs():
  """Every project should have a `documentation.md` file inside."""
  projects = os.listdir(projects_folder())

  for project_id in projects:
    print("Checking:", project_id)
    assert(os.path.exists(projects_folder(f"{project_id}/documentation.md")))


def check_all_projects_have_monitoring():
  """Every project should have a `monitoring.csv` file."""
  projects = os.listdir(projects_folder())

  for project_id in projects:
    print("Checking:", project_id)
    assert(os.path.exists(projects_folder(f"{project_id}/monitoring.csv")))


def check_all_projects_have_valid_monitoring():
  """Every project should have the right columns in its `monitoring.csv` file."""
  projects = os.listdir(projects_folder())

  for project_id in projects:
    print("Validating monitoring for:", project_id)
    df = pd.read_csv(projects_folder(f"{project_id}/monitoring.csv"))

    print("Checking required columns")
    for col in MINIMAL_MONITORING_COLUMNS:
      print(col)
      assert(col in df.columns)

    print("Checking that all columns are allowed")
    for col in df.columns:
      print(col)
      assert(col in ALLOWED_MONITORING_COLUMNS)

    print("Checking that at least one monitoring period exists")
    assert(len(df) > 0)
