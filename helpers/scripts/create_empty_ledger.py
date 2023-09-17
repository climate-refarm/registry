import pandas as pd

import sys, os
sys.path.extend([".", "..", "../.."])
from helpers.models.credit import Credit
from helpers.utils.paths import ledger_folder


for field in Credit.model_fields:
  df = pd.DataFrame(columns=Credit.model_fields)

  if os.path.exists(ledger_folder("main.csv")):
    raise FileExistsError("Ledger already exists, exiting")

  else:
    print("Creating empty ledger")
    df.to_csv(ledger_folder("main.csv"), index=False)
