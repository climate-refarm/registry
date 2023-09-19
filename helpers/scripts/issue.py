import argparse
import json
import pandas as pd
from datetime import datetime

import sys
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import CreditStatus, Credit, CreditIssuer, CreditMethodology, CreditType
from helpers.utils.paths import ledger_folder


if __name__ == "__main__":
  """Command line utility for ISSUING credits into the main ledger.

  Usage:

  ```bash
  # Issues 19 credits from PR00002 with a status of `pre_issued`:
  python issue.py --n 19 --project_id PR00002 --status pre_issued
  ```
  """
  parser = argparse.ArgumentParser(description="Issue credits into the main ledger")
  parser.add_argument("--n", type=int, required=True, help="How many credits to issue")
  parser.add_argument("--project_id", type=str, required=True, help="The project ID that generated these credits")
  parser.add_argument("--status", type=str, choices=[CreditStatus.issued, CreditStatus.pre_issued, CreditStatus.retired, CreditStatus.pre_retired], default=CreditStatus.issued)
  args = parser.parse_args()

  df = pd.read_csv(ledger_folder("main.csv"), index_col="serial_number")
  print(f"Highest serial number found is '{df.index.max()}'")
  start = int(df.index.max().replace("CR", "")) + 1
  end = start + args.n

  serial_numbers = [f"CR{n:010d}" for n in range(start, end + 1)]

  print(f"Issuing credit range '{serial_numbers[0]}' to '{serial_numbers[-1]}'")

  to_add = []
  for sn in serial_numbers:
    if sn in df.index:
      print(f"WARNING: The serial number {sn} is already in the ledger, so it will be skipped")

    credit = Credit(
      serial_number=sn,
      issued_by=CreditIssuer.CLIMATE_REFARM_PBC,
      project_id=args.project_id,
      status=args.status,
      type=CreditType.AVOIDED_TON_CO2,
      methodology=CreditMethodology.OUR_SUSTAINABLE_FOOD_PROCUREMENT,
      date_issued=str(datetime.utcnow().date()),
      date_retired=None
    )

    to_add.append(json.loads(credit.model_dump_json()))

  df = pd.concat([df, pd.DataFrame(to_add).set_index("serial_number")])
  print("Updated ledger:")
  print(df)

  df.to_csv(ledger_folder("main.updated.csv"))
