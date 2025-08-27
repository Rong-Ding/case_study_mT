# Src Folder

## Purpose
Contains utility modules used across notebooks and scripts. These modules organise commonly used functions for trial parsing, prompt building, LLM calls, and API support.

## Contents
- `analyse_utils.py` → helper functions for enrollment info extraction by calling API, and analysis (e.g., average computation).
- `api_utils.py` → helpers for building FastAPI endpoints and structuring responses, e.g., accessing patient records with ID.
- `trialsearch_utils.py` → functions for building LLM prompts, calling LLMs, and processing and structuring eligibility scores.

## How to Use
- Import these modules in notebooks or scripts (setup code available in the notebooks). For example:
```python
from src.trialsearch_utils import build_prompt, get_enrollment
