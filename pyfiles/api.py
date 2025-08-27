# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 15:05:04 2025

@author: lenovo
"""

#%% modules
import os
import sys
f_path = '~/'
sys.path.append(f_path+'case_study_mT/') # Add data folder to path; adapt this for your own use
sys.path.append(f_path+'case_study_mT/src/') # helper functions in utils
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from typing import List

#import importlib
sys.path.append(f_path+'case_study_mT/notebooks/')
from app.model import PatientTrialMatches, TrialMatch
sys.path.append(f_path+'case_study_mT/src/')
#import api_utils
#importlib.reload(api_utils)
from api_utils import load_patient_by_id

#%% Endpoint to list patients

# Endpoint building
app = FastAPI(title="Trial Search AI Prototype")

@app.get("/patients", response_model=List[str])
def list_patients(folder_path=f_path+"case_study_mT/"):
  """
  List all available patient IDs based on file(name)s in the folder.
  """
  return [
      f.split("_")[1].split(".")[0]
      for f in os.listdir(folder_path)
      if f.startswith("patient_") and f.endswith(".json")
  ]

# Endpoint setup test
client = TestClient(app)

# Test "/patients" endpoint
response = client.get("/patients")
print("Status code:", response.status_code) # 200 means success
print("Response JSON:", response.json()) # Expected: ['01', '02', '03'] or alike

#%% Endpoint to retrieve eligibility scores for a given patient (ongoing)

# Endpoint building
@app.get("/patients/{patient_id}/trials", response_model=PatientTrialMatches)
def get_eligibility_scores(patient_id: str):
  """
  Retrieve eligibility scores for a given patient across relevant trials.
  """
  patient = load_patient_by_id(patient_id)
  if not patient: # if the patient cannot be found
    raise HTTPException(status_code=404, detail="Patient not found")
  pass # For later: would add access to the saved json datafile with patient-trial matching results
  #return PatientTrialMatches(patient_id=patient_id, trial_matches=trial_matches)