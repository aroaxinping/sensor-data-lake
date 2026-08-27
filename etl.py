"""Fetch hourly weather and land it as Parquet in S3."""

import argparse
import io

import boto3
import pandas as pd
import requests
import yaml

with open("settings.yaml") as fh:
    CFG = yaml.safe_load(fh)

# Rough city -> lat/lon lookup for the demo.
CITIES = {
    "Barcelona": (41.39, 2.16),
    "Madrid": (40.42, -3.70),
}


def fetch(city: str) -> pd.DataFrame:
    lat, lon = CITIES[city]
    resp = requests.get(
        CFG["source"]["api"],
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join(CFG["source"]["variables"]),
        },
        timeout=30,
    )
    resp.raise_for_status()
    return pd.DataFrame(resp.json()["hourly"])


def land(df: pd.DataFrame, city: str) -> None:
    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    buf.seek(0)
    s3 = boto3.client(
        "s3",
        aws_access_key_id=CFG["aws"]["access_key_id"],
        aws_secret_access_key=CFG["aws"]["secret_access_key"],
        region_name=CFG["aws"]["region"],
    )
    key = f"{CFG['sink']['prefix']}{city.lower()}.parquet"
    s3.put_object(Bucket=CFG["sink"]["bucket"], Key=key, Body=buf.getvalue())
    print(f"landed s3://{CFG['sink']['bucket']}/{key} ({len(df)} rows)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", default="Barcelona")
    args = parser.parse_args()
    land(fetch(args.city), args.city)


if __name__ == "__main__":
    main()
