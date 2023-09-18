from pydantic import BaseModel
from datetime import datetime

from helpers.utils.git import get_head_commit_sha


class ClimateOffsetPortfolioSummary(BaseModel):
  """Represents the high-level impact metrics for the Climate Offset Portfolio.

  Notes
  -----
  In the future, we may add additional impact metrics to track other aspects of
  our projects.
  """
  updated_at: str = datetime.utcnow().isoformat() + "Z"
  commit_sha: str = get_head_commit_sha()

  total_credits_issued: float
  total_emission_reductions_tons_co2: float
  total_land_use_reduced_ha: float
  total_land_restored_ha: float
  total_land_conserved_ha: float
  total_animal_lives_saved: float
  total_meals_impacted: float
