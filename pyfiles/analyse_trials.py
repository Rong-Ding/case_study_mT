# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 14:43:30 2025

@author: lenovo
"""

#%% modules
import sys
f_path = '~/'
sys.path.append(f_path+'case_study_mT/') # Add data folder to path; adapt this for your own use
sys.path.append(f_path+'case_study_mT/src/') # helper functions in utils
import json
import pandas as pd
import requests
from collections import Counter

sys.path.append(f_path+'case_study_mT/src/') # for helper functions
#import importlib
#import analyse_utils
#importlib.reload(analyse_utils)
from analyse_utils import get_enrollment, compute_average_enrollment

#%% Read in and transform payloads data
records = []
file_path = f_path+'case_study_mT/payloads.jsonl'
with open(file_path, "r") as f:
  for line in f:
    records.append(json.loads(line))
    
# Convert to DataFrame for easier exploration
df_rec = pd.DataFrame(records)
# Show some rows as an example if wanted
#print(df_rec.head())

#%% Question 1: How many Phase 1, Phase 2, and Phase 3 trials are there?

# Count what types of phase are there, and how many trials each type
counts = df_rec['phase'].astype(str).value_counts().reset_index() # create a new dataframe by counting the number of each level of phase
counts.columns = ['Phase', 'Count'] # modify the name of each column for understanding
print(counts) # to visualise phases and their numbers

#%% Question 2: What is the average number of (Estimated) Enrollments for each phase?

# Sanity check: any column(s) that provides enrolment info?
#print(df_rec.columns) # The answer is not really if you print them; nothing enrollment related

# Compute the average actual and estimated enrollments per Phase
phases = [['Phase '+str(i)] for i in range(1,4)]

df_sample = pd.DataFrame() # to store all the trial entries used for later check if needed
df_avg = pd.DataFrame() # to store the average enrollment
for phase in phases:
  df_sample_phase = pd.DataFrame()
  df_avg_phase = pd.DataFrame()

  # Select first 10 trials per phase
  df_sample_phase = df_rec[df_rec['phase'].apply(lambda x: x==phase)].head(10)
  # Add one column (enrollment_info) per row/entry on top of the original dataset
  df_sample_phase['enrollment_info'] = df_sample_phase['utn'].apply(get_enrollment)
  # Compute the avgs
  df_avg_phase = compute_average_enrollment(df_sample_phase)
  # Add the phase data to the bigger df
  df_sample = pd.concat([df_sample, df_sample_phase])
  df_avg = pd.concat([df_avg, df_avg_phase])

df_avg.columns = ['Phase', 'Enrollment Type', 'Average Enrollment', 'Number of Trials Used']
df_sample = df_sample.reset_index()
#print(df_sample) # to visualise for a check
print(df_avg) # to print the answer to the question (as a dataframe corresponding each phase with an actual and estimated avg)

#%% Question 3: What are the top 10 most commonly studied conditions?

# Run through all trials and record all terms and their frequencies using Counter
condition_counter = Counter()

for terms in df_rec['mesh_terms']:
  if isinstance(terms, list):
    for t in terms:
      term_name = t.get('term')
      if term_name:
        condition_counter[term_name] += 1

# Get the most common 10 conditions
top_conditions = condition_counter.most_common(10)
for condition, count in top_conditions:
  print(f"{condition}: {count}")
  
#%% Save the dataset (only Phase 1, 2, or 3 trials) for further use in Part 2
phases = [['Phase '+str(i)] for i in range(1,4)]
df_rec_phases = pd.DataFrame()
for phase in phases:
  df_single_phase = df_rec[df_rec['phase'].apply(lambda x: x==phase)]
  df_rec_phases = pd.concat([df_rec_phases, df_single_phase])

df_rec_phases.to_pickle(f_path+'case_study_mT/df_rec_phases.pkl')