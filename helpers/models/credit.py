from pydantic import BaseModel
from enum import Enum
from typing import Optional


class CreditIssuer(str, Enum):
  """Standardized names for different credit issuers.

  Notes
  -----
  A credit issuer is the registry where a carbon credit is tracked. Some credits
  are issued by an external registry (e.g Verra) but tracked in our system for
  the sake of bookkeeping in one place.
  """
  CLIMATE_REFARM_PBC = "CLIMATE_REFARM_PBC"


class CreditStatus(str, Enum):
  """Represents the lifecycle stage of a credit.

  Notes
  -----
  * An `issued` credit has been created but not yet sold
  * A `retired` credit has been sold and marked as inactive so that it can't be double counted
  * A `pre_issued` credit has been created based on the *projected* impact of a project. Pre-issued
    credits will always be replaced by `issued` credits eventually.
  * A `pre_retired` credit has been sold based on the *projected* impact of a project, and is used
    to provide up-front funding for that project. Pre-retired credits will always be replaced by
    `retired` credits eventually.
  """
  issued = "issued"
  retired = "retired"

  pre_issued = "pre_issued"
  pre_retired = "pre_retired"


class CreditType(str, Enum):
  """Represents a type of credit.

  Notes
  -----
  Credits can have many different attributes. At the simplest level, a credit
  can represent avoided emissions, carbon removal, or a mix of both. In the
  future, we may separate these credit types into subcategories, such as
  reversible or irreversible avoided emissions.
  """
  AVOIDED_TON_CO2 = "A"
  REMOVAL_TON_CO2 = "R"
  MIXED_TON_CO2 = "M"


class CreditMethodology(str, Enum):
  """The methodology by which this credit was issued and verified."""
  # Written by Climate Refarm, PBC. Publication forthcoming.
  OUR_SUSTAINABLE_FOOD_PROCUREMENT = "M1"


class Credit(BaseModel):
  """Represents a credit that is tracked on our main ledger."""
  serial_number: str
  issued_by: CreditIssuer

  project_id: str
  status: CreditStatus

  type: CreditType
  methodology: CreditMethodology

  date_issued: str
  date_retired: Optional[str] = None
