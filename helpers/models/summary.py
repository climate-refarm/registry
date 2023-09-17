from pydantic import BaseModel
from datetime import datetime


class ClimateOffsetPortfolioSummary(BaseModel):
  """Represents the high-level impact metrics for the Climate Offset Portfolio."""
  # Be default, use the current UTC time.
  updated_at: str = datetime.utcnow().isoformat() + "Z"

  total_credits_issued: float
  total_emission_reductions_tons_co2: float
  total_land_use_reduced_ha: float
  total_land_restored_ha: float
  total_land_conserved_ha: float
  total_animal_lives_saved: float
