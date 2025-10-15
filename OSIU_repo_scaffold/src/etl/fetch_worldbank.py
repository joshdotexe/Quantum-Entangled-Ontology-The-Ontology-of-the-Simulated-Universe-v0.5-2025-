
import argparse
import time
import requests
import pandas as pd
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start}:{end}&format=json&per_page=20000"

def _session_with_retries(total=5, backoff_factor=0.8, status_forcelist=(429, 500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=total,
        read=total,
        connect=total,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_indicator(country, indicator, start, end, timeout=60, session: requests.Session | None = None):
    url = API.format(country=country, indicator=indicator, start=start, end=end)
    sess = session or _session_with_retries()
    r = sess.get(url, timeout=timeout)
    r.raise_for_status()
    js = r.json()
    if not isinstance(js, list) or len(js) < 2:
        return pd.DataFrame()
    rows = js[1] or []
    df = pd.DataFrame([
        {"region": row.get("country", {}).get("id"),
         "year": int(row["date"]),
         "value": float(row["value"]) if row["value"] is not None else None}
        for row in rows
    ])
    return df.dropna()

def main(config_path: str, outdir: str = "data/raw"):
    import yaml
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(Path(config_path).read_text())
    wb = cfg.get("worldbank", {})
    start = wb.get("start_year", 2000)
    end = wb.get("end_year", 2024)
    countries = wb.get("countries", ["USA"])
    indicators = wb.get("indicators", [{"code": "GE.EST"}])
    sess = _session_with_retries()

    for ind in indicators:
        code = ind["code"]
        for c in countries:
            try:
                df = fetch_indicator(c, code, start, end, session=sess)
            except requests.exceptions.RequestException as e:
                print(f"WARN: World Bank fetch failed for {c} {code}: {e}")
                continue
            if df.empty:
                print(f"INFO: No data for {c} {code}")
                continue
            df["id"] = f"worldbank_{code}"
            fp = out / f"worldbank_{code}_{c}.csv"
            df.to_csv(fp, index=False)
            time.sleep(0.5)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--outdir", default="data/raw")
    args = ap.parse_args()
    main(args.config, args.outdir)
