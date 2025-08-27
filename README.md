## 🧪 Clinical Trial Eligibility Matching Prototype
This repository features a prototype system for matching patients to clinical trials using Large Language Models (LLMs). An ETL pipeline to analyse and transform trial data and a prototype for API data endpoints are also available.

## Repository Structure
- _data/_ : Contains datasets and results.
  - Saved eligibility results across trials per patient (`Results_eligibility.json`)
- _notebooks/_ : Prototyping and analysis in Google Colab/Jupyter.
  - `analyse_trials.ipynb` → trial data exploration and cleaning
  - `TrialSearch_prototype.ipynb` → main pipeline for patient–trial matching
  - `api.ipynb` → prototype FastAPI service tested in Colab
- _pyfiles/_ : Python exports of the notebooks (cleaner scripts for reference).
- _src/_ : Utility modules (with helper functions) used by notebooks and API.
  - `analyse_utils.py` → functions for parsing and analysing trial data
  - `api_utils.py` → helpers for FastAPI endpoints
  - `trialsearch_utils.py` → functions for building prompts, calling LLMs

## Reproducing Results
The quickest way to reproduce or skim results is via **Google Colab notebooks**:

0. Requirements: Google account, access to Google Drive (and mounted at `/content/drive/`; see setup code inside each notebook)
    - **Important note**: data files needed for the analysis (i.e., trial data, indexing records, and patient profiles) are currently not accessible in this repository. However, if you have the data (anonymised), you could easily upload them to your personal drive and put them under the same folder with the notebooks (e.g., _/content/drive/MyDrive/Projects/case_study_mT/_) to set the pipeline to work.
1. Explore trial data
   - Open `analyse_trials.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Rong-Ding/case_study_mT/blob/main/notebooks/analyse_trials.ipynb)
   - This notebook:
     - Explores and preprocesses the clinical trial dataset
     - Loads enrollment info via clinicalgov.com API
     - Saves filtered trial records as metadata
2. Run the patient–trial matching pipeline
   - Open `TrialSearch_prototype.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Rong-Ding/case_study_mT/blob/main/notebooks/TrialSearch_prototype.ipynb)
   - This notebook:
     - Loads the metadata generated from raw trial data, indexing records (i.e., `indexing_records.csv`) and patient profiles (e.g., `patient_01.json`, `patient_02.json`, etc.)
     - Search trial data related to Duchenne Muscular Dystrophy based on **NCT-numbers**
     - Builds prompts and calls the LLM (`GPT-4.1-mini`) to summarise and score eligibility for Duchenne Muscular Dystrophy, matching patients with trials
     - Saves results in structured JSON (`Results_eligibility.json`)
3. Try the API prototype
   - Open `api.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Rong-Ding/case_study_mT/blob/main/notebooks/api.ipynb)
   - Demonstrates how to wrap the pipeline into a FastAPI service with endpoints for **Listing patients** and **Querying eligibility scores** per patient (ongoing).

If you prefer to go through the pipelines/results locally instead of Colab, follow these steps:
0. Requirements: Python 3.9+, [pip](https://pip.pypa.io/en/stable/) (or `conda`), and an OpenAI API key (for LLM calls, if you want to re-run eligibility scoring)
1. Clone the repository
 ```bash
   git clone https://github.com/Rong-Ding/case_study_mT.git
   cd case_study_mT
```

2. 
3. 

