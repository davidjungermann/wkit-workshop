# Amalone Books Python API

## Setup

1. Install dependencies:
```console
pip install -r requirements.txt && pip install -r requirements-dev.txt
```

2. Run FastAPI server:
```console
uvicorn main:app --reload
```

3. Ensure that everything works, in a new terminal write
```console
curl 127.0.0.1:8000/health
```

Ensure that you get `OK` back.

4. Run tests:
```console
pytest test.py
```

5. Populate database:
```console
python populate.py
```

6.
Ensure you get products:
```console
curl 127.0.0.1:8000/products/
```

## Build with
This API is built using:
* Fast API
* SQLAlchemy
* Pydantic

## Tooling
There's a pre-commit hook configured, that can be installed by:

```console
pre-commit install
```

Run it for all files:
```console
pre-commit run --all
```

This uses **Black** for formatting, **isort** for import formatting and **mypy** for static linting and type checking. 

## TODO
- Add CI/CD for deployment
- Run tests remotely in a Github Action
- Update Pydantic typing to match new version of SQLAlchemy typing
- Set up dedicated test database for integration testing
- Extend unit tests to reach higher coverage


