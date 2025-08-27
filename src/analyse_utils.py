import requests
import pandas as pd

def get_enrollment(nct_id):
  """
  Function to get enrollment info from data by calling API.
  Input (str): NCT-id per entry under variable/column "utn", e.g. NCT05680818
  Output (dict): Enrollment info containing count and type of enrollment, e.g. {'count': 136, 'type': 'ESTIMATED'}
  """
  url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}"
  try: # access the API
    r = requests.get(url, timeout=10)  # set timeout for network reliability
    r.raise_for_status()  # raise HTTPError for bad status codes
  except requests.exceptions.RequestException as e:
    print(f"Request error for {nct_id}: {e}")
    return None

  data = r.json()

  try: # get enrollment info
    enrollment_info = data.get("protocolSection", {}) \
                    .get("designModule", {}) \
                    .get("enrollmentInfo", {})
    return enrollment_info
  except Exception as e: # in case the info is missing
    print(f"Unexpected structure for {nct_id}: {e}")
    return None

def compute_average_enrollment(df):
  """
  Function to compute the average enrollment per phase.
  Input (pd dataframe): a dataframe containing selected trials, including a column (enrollment_info) with count and type as a dict
  Ouput (pd dataframe): a dataframe containing the average enrollment per phase, actual and estimated
  """
  # For easier computation, split the enrollment column into two more columns, count and type
  df['enrollment_count'] = df['enrollment_info'].apply(lambda x: x.get('count') if isinstance(x, dict) else None)
  df['enrollment_type'] = df['enrollment_info'].apply(lambda x: x.get('type') if isinstance(x, dict) else None)
  # Identify and drop rows with missing enrollment info (e.g., NaN)
  df['enrollment_count'] = pd.to_numeric(df['enrollment_count'], errors='coerce') # to mark NaN or missing data
  # Tranform the list var into str for better visualisation
  df['phase_clean'] = df['phase'].apply(lambda x: x[0])
  # Group by cleaned phase + enrollment type
  result = (
        df.groupby(['phase_clean', 'enrollment_type'])
          .agg(
            avg_enrollment=('enrollment_count', 'mean'),
            n_trials_used=('enrollment_count', 'count')  # number of non-NaN rows (i.e., actual trials considered)
          )
          .reset_index()
    )
  return result