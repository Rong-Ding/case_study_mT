# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 14:54:44 2025

@author: lenovo
"""
#%% modules
from google.colab import userdata
api_key = userdata.get('OPENAI_API_KEY_mT') # for openai calling
import sys
f_path = '~/'
sys.path.append(f_path+'case_study_mT/') # Add data folder to path; adapt this for your own use
sys.path.append(f_path+'case_study_mT/src/') # helper functions in utils
import json
import pandas as pd
from openai import OpenAI

#import importlib
#import trialsearch_utils
#importlib.reload(trialsearch_utils)
from trialsearch_utils import get_eligibility_text, load_json, patient_to_text, trial_to_text, build_prompt, call_llm

#%% Load the dataframe files
df_trials = pd.read_pickle(f_path+'case_study_mT/df_rec_phases.pkl')
#print(df_trials.head())

#%% Question 1: Within the disease “Duchenne Muscular Dystrophy”, what are the common eligibility criteria?

# Filter trials for DMD using trial indexing

# Read in the indexing record file with NCT-disease pairs
index_file = f_path+'case_study_mT/indexing_records.csv'
df_index = pd.read_csv(index_file)
#print(df_index.head())

# Find all NCT-numbers associated with DMD
dmd_ncts = df_index[df_index['a.alias'] == "Muscular Dystrophy, Duchenne"]['s.id'].tolist()
print(f"Found {len(dmd_ncts)} DMD-related NCT numbers")

# Find all relevant trials to DMD in the dataset
relevant_trials = df_trials[df_trials['utn'].isin(dmd_ncts)]
print(f"Found {len(relevant_trials)} DMD-related trials in the dataset")
#relevant_trials.iloc[14]["eligibility"] - by some initial eyeballing, inclusion and exclusion texts are often the same
#print(relevant_trials[['utn', 'phase', 'eligibility']].head()) # check results
#get_eligibility_text(relevant_trials.iloc[6]["eligibility"])

# Add two columns (inclusion and exclusion) to the dataset
relevant_trials[['inclusion_text', 'exclusion_text']] = relevant_trials['eligibility'].apply(
    lambda x: pd.Series(get_eligibility_text(x))
)
# Then, gather all inclusion and exclusion texts (if any) separately for prompt prep
# Combine all inclusion criteria
all_inclusion = " ".join([text for text in relevant_trials['inclusion_text'] if text])
# Combine all exclusion criteria - there is no exclusion text left as they are all identical to inclusion
#all_exclusion = " ".join([text for text in relevant_trials['exclusion_text'] if text])

# Prompt to ask LLM for criterion summarisation
prompt = f"""
You are a clinical trial assistant.

Here are the combined inclusion criteria from Duchenne Muscular Dystrophy clinical trials:
{all_inclusion}

Please provide your answer as bullet points, each describing one common eligibility criterion.
Focus on the key patterns that appear across multiple trials.
"""

# Call the LLM via OpenAI API
client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
  model="gpt-4.1-mini",
  messages=[{"role": "user", "content": prompt}],
  temperature=0.3,
  #max_tokens=8000
)

# Extract and print the text
summary = response.choices[0].message.content
print(summary)

#%% Question 2: Match Patients to Trials

# Read in one participant file for a look
#file_path = "/content/drive/MyDrive/Projects/case_study_mT/patient_02.json"
#record = load_json(file_path)
#record
#patient_to_text(record)

# json data for patients
patients = ["01", "02", "03"]
#patients = ["02",] # for unit test
file_path = f_path+'case_study_mT/'

# Estimate patient-trial eligibility per patient across trials
Results = {}
for id in patients:
  # Load file
  patient_file = file_path + "patient_{}.json".format(id)
  patient_data = load_json(patient_file)
  
  # Create the structure for the current patient
  Results[id] = {
    "patient_info": patient_data,
    "trial_matches": []
  }
  
  for trial_inx in range(len(relevant_trials)):
  #for trial_inx in range(0,2): # as a tryout # for unit test
    trial = relevant_trials.iloc[trial_inx]
    nct_id = trial.get("utn")
    prompt = build_prompt(patient_data, trial)
    
    try:
      match_result = call_llm(prompt)
      Results[id]["trial_matches"].append({
        "nct_id": nct_id,
        "eligibility": match_result.get("eligibility"),
        "reasoning": match_result.get("reasoning")
      })
    except Exception as e: # if in strange cases no eligibility info available
      Results[id]["trial_matches"].append({
        "nct_id": nct_id,
        "eligibility": "error",
        "reasoning": str(e)
      })

# # Showcase results of one patient
print(Results["03"])


#%% Save the Results for downstream API building
with open(file_path + 'Results_eligiblity.json', 'w') as fp:
  json.dump(Results, fp)