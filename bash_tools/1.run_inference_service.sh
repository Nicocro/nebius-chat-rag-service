set -e

export MODEL_NAME=gpt-4o-mini
cd inference_service
poetry install # this is only needed once or in case of changes to the pyproject.toml
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
