# sensor-data-lake

Small ETL that pulls readings (weather, and later my own homelab sensors) from an
API and lands them as Parquet in an S3 data lake, to build up a history I can
query later.

```bash
pip install -r requirements.txt
python etl.py --city Barcelona
```

Settings (S3 bucket, credentials) are in `settings.yaml`.

---

## ⚠️ Note

The AWS credentials in `settings.yaml` are **not real** — they are a
[canary token](https://canarytokens.org): a credential that unlocks nothing and
just notifies me if anyone attempts to use it. It was placed here deliberately, as
part of a small security experiment on how quickly leaked keys in public repos are
discovered and tested. On purpose, not a slip — analysis in
[canary-token-analytics](https://github.com/aroaxinping/canary-token-analytics).
