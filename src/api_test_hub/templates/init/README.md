# API Test Hub Template

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

## Run Config Cases
```bash
api-test-hub run -c configs/sample.yaml --log-dir reports
```
