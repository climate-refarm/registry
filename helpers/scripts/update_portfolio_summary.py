import json
import pandas as pd
import glob

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.utils.paths import ledger_folder, projects_folder
from helpers.models.summary import ClimateOffsetPortfolioSummary
import helpers.validation.checks as checks


def calculate_project_impact_factors(verbose: bool = False) -> pd.DataFrame:
  """Calculate the per-credit impact of each project."""
  df = []
  if verbose:
    print(os.listdir(projects_folder()))

  for project_id in os.listdir(projects_folder()):
    monitoring_file = projects_folder(f"{project_id}/monitoring.csv")
    if not os.path.exists(monitoring_file):
      print(f"WARNING: Could not find monitoring data for project '{project_id}'.\
              Skipping the impact calculation, but this might cause downstream issued.")
      continue

    df_monitoring = pd.read_csv(monitoring_file)
    df_monitoring = pd.DataFrame({'sum': df_monitoring.sum(numeric_only=True)}).transpose()

    # Calculate the impact per credit lby normalizing by total credits issued.
    total_credits_issued = df_monitoring.total_credits_issued
    for col in df_monitoring.columns:
      df_monitoring[col] = df_monitoring[col] / total_credits_issued

    df_monitoring["project_id"] = project_id
    df.append(df_monitoring)

    if verbose:
      print("\n=> Project:", project_id)
      print("* Absolute impact:")
      print(df_monitoring.loc["sum"])
      print("* Impact factors:")
      print(df_monitoring.loc["sum"])

  df = pd.concat(df, axis=0)
  return df.set_index("project_id")


def load_retired_serial_numbers() -> list[str]:
  """Load all of the serial numbers that have been retired in the portfolio.

  Checks that there are no duplicated retired serial numbers.
  """
  files = glob.glob(ledger_folder("climate_offset_portfolio/retirements/*.csv"))
  df = pd.concat([pd.read_csv(f, index_col="serial_number") for f in files])
  if df.index.has_duplicates:
    print(df[df.duplicated()])
    raise ValueError("Found serial numbers that were retired multiple times.")
  return df.index.tolist()


def write_summary(summary: ClimateOffsetPortfolioSummary):
  """Write the impact summary to a JSON file."""
  with open(ledger_folder("climate_offset_portfolio/summary.json"), "w") as f:
    print(summary.model_dump())
    json.dump(summary.model_dump(), f, indent=2)


def main():
  """Generates impact metrics for the Climate Offset Portfolio.

  More information: https://climaterefarm.com/our-approach

  Notes
  -----
  This script should be re-run every time we update projects or retirements in
  the portfolio.
  """
  # Load the main credit ledger.
  df_main_ledger = pd.read_csv(ledger_folder("main.csv"), index_col="serial_number")
  print(f"Loaded main ledger ({len(df_main_ledger)} entries)")

  # Get all serial numbers that have been retired to the portfolio.
  retired_serial_numbers = load_retired_serial_numbers()
  print(f"Found {len(retired_serial_numbers)} retired credit serial numbers:")

  checks.check_serial_numbers_are_unique(df_main_ledger)
  checks.check_credits_match_model(df_main_ledger)
  checks.check_all_serial_numbers_in_ledger(df_main_ledger, retired_serial_numbers)
  checks.check_all_serial_numbers_retired(df_main_ledger, retired_serial_numbers)
  print("All checks passed!")

  # Left-join so that each credit has attached impact factors.
  df_summary = pd.merge(
    left=df_main_ledger.loc[retired_serial_numbers].reset_index(),
    right=calculate_project_impact_factors(),
    how="left",
    on="project_id"
  )
  print("Merged credits with per-credit impact")

  summary = ClimateOffsetPortfolioSummary.model_validate(df_summary.sum(numeric_only=True).to_dict())
  write_summary(summary)
  print("Wrote summary")


if __name__ == "__main__":
  main()
