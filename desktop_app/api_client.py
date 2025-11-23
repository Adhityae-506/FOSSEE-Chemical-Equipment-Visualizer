# desktop_app/api_client.py
import requests

# Same backend you use for React
API_BASE = "http://127.0.0.1:8000/api"


class ApiError(Exception):
    pass


def _handle_response(r: requests.Response):
    try:
        r.raise_for_status()
    except requests.RequestException as e:
        # Try to include backend error detail if present
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = None
        msg = detail or str(e)
        raise ApiError(msg)
    try:
        return r.json()
    except ValueError:
        return r.content


def upload_csv(path: str):
    """
    Upload a CSV file to /api/datasets/upload/
    Returns JSON with summary.
    """
    url = f"{API_BASE}/datasets/upload/"
    with open(path, "rb") as f:
        files = {"file": f}
        r = requests.post(url, files=files, timeout=60)
    return _handle_response(r)


def get_latest_summary():
    """
    GET /api/datasets/latest/
    """
    url = f"{API_BASE}/datasets/latest/"
    r = requests.get(url, timeout=30)
    return _handle_response(r)


def get_history():
    """
    GET /api/datasets/history/
    """
    url = f"{API_BASE}/datasets/history/"
    r = requests.get(url, timeout=30)
    return _handle_response(r)


def download_report(save_path: str) -> str:
    """
    GET /api/datasets/latest/report/ and save to 'save_path'.
    Returns the final path.
    """
    url = f"{API_BASE}/datasets/latest/report/"
    r = requests.get(url, stream=True, timeout=60)

    try:
        r.raise_for_status()
    except requests.RequestException as e:
        # Try to surface backend error JSON if any
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = None
        msg = detail or str(e)
        raise ApiError(msg)

    with open(save_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return save_path
