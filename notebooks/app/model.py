from pydantic import BaseModel
from typing import List, Optional

class Patient(BaseModel): # List patients
  id: str
  profile: dict

class TrialMatch(BaseModel): # Retrieve eligiblity scores for one trial
  nct_id: str
  eligibility: str
  reasoning: Optional[str] = None # in case there's no reasoning description

class PatientTrialMatches(BaseModel): # eligiblity scores for all trials per participant
  patient_id: str
  trial_matches: List[TrialMatch]