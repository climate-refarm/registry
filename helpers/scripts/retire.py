import argparse
from datetime import datetime
import pandas as pd

import sys
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import CreditStatus
from helpers.utils.paths import ledger_folder


if __name__ == "__main__":
  """Command line utility for RETIRING credits into the portfolio.

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
  parser.add_argument("--status", type=str, required=True, choices=[CreditStatus.retired, CreditStatus.pre_retired], help="What status to assign the credits that are being retired")
  args = parser.parse_args()

  if args.start > args.end:
    raise ValueError("Invalid range")

  df = pd.read_csv(ledger_folder("main.csv"), index_col="serial_number")

  print("Writing backup main ledger")
  df.to_csv(ledger_folder("backup.main.csv"))

  serial_numbers = [f"CR{n:010d}" for n in range(args.start, args.end + 1)]

  print(f"Retiring credit range '{serial_numbers[0]}' to '{serial_numbers[-1]}'")

  df_retired = pd.read_csv(ledger_folder(f"climate_offset_portfolio/retirements/{args.to}"), index_col="serial_number")

  # Write a backup in case we want to roll back the change.
  df_retired.to_csv(ledger_folder(f"climate_offset_portfolio/retirements/backup.{args.to}"))

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

    # Update the main ledger.
    df.loc[sn].status = args.status
    df.loc[sn].date_retired = str(datetime.utcnow().date())

  df_retired_updated = pd.DataFrame({"serial_number": sorted(list(retired_serials))})
  df_retired_updated.to_csv(ledger_folder(f"climate_offset_portfolio/retirements/{args.to}"), index=False)
  print("Wrote a new retirements file. Inspect it before committing!")

  df.to_csv(ledger_folder("main.csv"))
  print("Wrote updated main ledger")
