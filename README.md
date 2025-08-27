## 🧪 Clinical Trial Eligibility Matching Prototype
This repository features a prototype system for matching patients to clinical trials using Large Language Models (LLMs). An ETL pipeline to analyse and transform trial data and a prototype for API data endpoints are also available.

## Repository Structure
- _data/_ : Contains datasets and results.
  - Saved eligibility results (`Results_eligibility.json`)
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
1. Explore trial data using `analyse_trials.ipynb` [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Rong-Ding/case_study_mT/blob/main/notebooks/analyse_trials.ipynb)
