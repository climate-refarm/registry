from pydantic import BaseModel
from enum import Enum


class CreditIssuer(str, Enum):
  CLIMATE_REFARM_PBC = "CLIMATE_REFARM_PBC"


class CreditStatus(str, Enum):
  """Represents the lifecycle stage of a credit."""
  issued = "issued"
  retired = "retired"

  pre_issued = "pre_issued"
  pre_retired = "pre_retired"


class CreditType(str, Enum):
  """Represents a type of credit."""
  AVOIDED_TON_CO2 = "1T.A"
  REMOVAL_TON_CO2 = "1T.R"
  MIXED_TON_CO2 = "1T.M"


class CreditMethodology(str, Enum):
  """The methodology by which this credit was issued and verified."""
  # Our sustainable food procurement methodology
  OUR_SUSTAINABLE_FOOD_PROCUREMENT = "M1"


class Credit(BaseModel):
  """Represents a credit that is tracked on the main ledger."""
  serial_number: str
  issued_by: CreditIssuer

  project_id: str
  status: CreditStatus

  type: CreditType
  methodology: CreditMethodology

  date_issued: str
  date_retired: str
