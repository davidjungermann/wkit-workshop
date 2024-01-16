# Amalone Books Python API

## Running in Codesandbox

1. Install dependencies:
```console
pip install -r requirements.txt
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
pytest .
```




## Prerequisites for local development
1. Install Python
2. Install all the dependencies
