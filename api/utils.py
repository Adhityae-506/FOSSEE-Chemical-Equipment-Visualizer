import pandas as pd
from io import StringIO, BytesIO

REQUIRED_COLUMNS = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature']

def read_file_content(file_obj):
    content = file_obj.read()
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            content = content.decode('latin1')
    return content

def parse_and_summarize_csv(file_obj):
    """
    Accepts a Django UploadedFile or file-like object.
    Returns (summary_dict, dataframe).
    Raises ValueError with message for invalid CSV.
    """
    try:
        content = read_file_content(file_obj)
        df = pd.read_csv(StringIO(content))
    except Exception as e:
        raise ValueError(f"CSV parsing error: {str(e)}") from e

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        if len(missing) == 1:
            raise ValueError(f"CSV parsing error: missing required column '{missing[0]}'")
        else:
            raise ValueError(f"CSV parsing error: missing required column(s) {', '.join(missing)}")

    # coerce numeric columns
    for col in ['flowrate', 'pressure', 'temperature']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().any():
            # find first bad row
            bad_idx = df[df[col].isnull()].index.tolist()
            raise ValueError(f"CSV parsing error: non-numeric values found in column '{col}' at rows {bad_idx}")

    total = int(len(df))
    avg_flow = round(float(df['flowrate'].mean()), 2)
    avg_pressure = round(float(df['pressure'].mean()), 2)
    avg_temp = round(float(df['temperature'].mean()), 2)
    type_dist = df['type'].value_counts().to_dict()

    summary = {
        "total_equipment": total,
        "average_flowrate": avg_flow,
        "average_pressure": avg_pressure,
        "average_temperature": avg_temp,
        "type_distribution": type_dist
    }
    return summary, df
