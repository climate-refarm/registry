import argparse
import os
import pandas as pd

import sys
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import CreditStatus
from helpers.utils.paths import ledger_folder


if __name__ == "__main__":
  """Command line utility for retiring credits into the portfolio.

  Usage:

  ```bash
  # Retires all credits betweeen CR0000000001 and CR0000000090, inclusive:
  python retire.py --start 1 --end 90 --to 202309.csv
  ```
  """
  parser = argparse.ArgumentParser(description="Retire credits into the portfolio")
  parser.add_argument("--start", type=int, required=True, help="The start of the serial number range")
  parser.add_argument("--end", type=int, required=True, help="The end of the serial number range")
  parser.add_argument("--to", type=str, required=True, help="A file relative to the retirements folder")
  args = parser.parse_args()

  if args.start > args.end:
    raise ValueError("Invalid range")

  df = pd.read_csv(ledger_folder("main.csv"), index_col="serial_number")

  serial_numbers = [f"CR{n:010d}" for n in range(args.start, args.end + 1)]
  print(serial_numbers)

  print(f"Retiring credit range '{serial_numbers[0]}' to '{serial_numbers[-1]}'")

  df_retired = pd.read_csv(ledger_folder(f"climate_offset_portfolio/retirements/{args.to}"), index_col="serial_number")
  retired_serials = set(df_retired.index.to_list())

  for sn in serial_numbers:
    if sn not in df.index:
      raise ValueError(f"The serial number {sn} has not been issued")

    status = df.loc[sn].status
    if status == CreditStatus.retired or status == CreditStatus.pre_retired:
      print(f"WARNING: {sn} has already been retired")

    if sn in retired_serials:
      print(f"WARNING: {sn} was already retired to the portfolio, so it won't be added again")

    retired_serials.add(sn)

  df_retired_updated = pd.DataFrame({"serial_number": sorted(list(retired_serials))})
  df_retired_updated.to_csv(ledger_folder(f"climate_offset_portfolio/retirements/{args.to}.updated.csv"), index=False)
  print("Wrote updated retirements file. Inspect it before renaming!")
