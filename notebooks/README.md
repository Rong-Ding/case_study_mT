# Notebooks Folder

## Purpose
Exploration of clinical trials, prototyping of the patient–trial matching pipeline, and creating/testing API endpoints for data access.

## Contents
- `TrialSearch_prototype.ipynb` → main patient–trial matching pipeline, includes LLM calls
- `analyse_trials.ipynb` → data analysis and cleaning
- `app/` → modular code for reproducibility
  - `model.py` → calling Pydantic base models to facilitate standardised API building
  - `api/` → folder containing API prototype
    - `api.ipynb` → testing FastAPI endpoints

## How to Use
1. Open the notebooks in **Google Colab**.
2. Mount your Google Drive to access datasets (e.g., trial data, indexing records, patient profiles).
3. Ensure required packages are installed:
   - `requirements_notebooks.txt` for Colab
   - `requirements.txt` for core dependencies
4. Run notebooks in order for smooth execution:
   - `analyse_trials.ipynb` → preprocess and explore trial data
   - `TrialSearch_prototype.ipynb` → match patients to trials
   - `app/api/api.ipynb` → test API endpoints
