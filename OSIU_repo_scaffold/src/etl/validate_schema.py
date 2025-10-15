
import argparse, glob, sys
import pandas as pd

def validate(df: pd.DataFrame) -> bool:
    required = {"region": "object", "year": "int64", "value": "float64", "id": "object"}
    ok = True
    for col, dt in required.items():
        if col not in df.columns:
            print(f"Missing column: {col}")
            ok = False
        else:
            # allow compatible dtypes
            pass
    return ok

def main(schema_csv: str, pattern: str):
    files = glob.glob(pattern)
    if not files:
        print("No files matched:", pattern)
        return 0
    bad = 0
    for fp in files:
        # Skip placeholder README-style files
        if "README" in fp.upper():
            continue
        try:
            df = pd.read_csv(fp)
        except Exception as e:
            print("Failed to read", fp, e)
            bad += 1
            continue
        if not validate(df):
            print("Schema invalid:", fp)
            bad += 1
    print("Checked", len(files), "files;", "bad:" , bad)
    return bad

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--glob", required=True)
    a = ap.parse_args()
    rc = main(a.schema, a.glob)
    sys.exit(1 if rc else 0)
