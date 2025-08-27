# Data Folder

## Purpose
Holds saved results, trial datasets (currently not available), patient JSON files (currently not available), and indexing records (currently not available).

## Contents
- `Results_eligibility.json` → saved trial eligibility results
  - **Purpose**: Stores the outcome of the patient–trial matching pipeline.
  - **Structure**: Hierarchical JSON mapping patients to their trials and results.
  - **Key Points**:
    - Top-level keys are **patient IDs** (e.g.,`01`, `02`, ...)
    - Each patient entry contains:
      - `profile` → patient details (e.g., age, gender, country)
      - `trials` → mapping of **NCT trial IDs** to their `eligibility` score and short `reasoning`.
    - Enables quick lookup of all trials for a given patient, or vice versa.

## How to Use
Place anonymised patient and trial data here for Colab notebooks to run correctly.

## Notes
As the filtered trial metadata from `analyse_trials.ipynb` (i.e., `df_rec_phases.pkl`) form a Large Dataset (>100MB), it is thus ignored by Git and must be stored locally.
