import pandas as pd

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import Credit, CreditStatus


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
