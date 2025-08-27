import os
import json

f_path = '~/'

def load_patient_by_id(patient_id: str, folder_path=f_path+'case_study_mT/'):
  """
  Load a single patient JSON file by ID.
  Returns the patient dict, or None if file is not found.
  """
  filename = f"patient_{patient_id}.json"
  file_path = os.path.join(folder_path, filename)

  if not os.path.exists(file_path):
    raise FileNotFoundError(f"Patient file '{filename}' not found in {folder_path}")

  with open(file_path, "r") as f:
    return json.load(f)