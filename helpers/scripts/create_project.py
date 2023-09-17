import argparse
import os
import pandas as pd

import sys
sys.path.extend([".", "..", "../.."])
from helpers.utils.paths import projects_folder
from helpers.validation.checks import MINIMAL_MONITORING_COLUMNS, ALLOWED_MONITORING_COLUMNS


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Generate a new empty project")
  parser.add_argument("--name", type=str, required=True, help="The project name to use")
  args = parser.parse_args()

  os.makedirs(projects_folder(args.name))
  print("Made new folder")

  with open(projects_folder(f"{args.name}/documentation.md"), "w") as f:
    f.write(f"# {args.name}")
  print("Made empty docs")

  df = {}

  for col in MINIMAL_MONITORING_COLUMNS:
    df[col] = []

  for col in ALLOWED_MONITORING_COLUMNS:
    df[col] = []

  pd.DataFrame(df).to_csv(projects_folder(f"{args.name}/monitoring.csv"), index=False)
  print("Made empty monitoring")
