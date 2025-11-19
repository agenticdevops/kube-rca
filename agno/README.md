Setup venv with uv

```
uv venv --python 3.11
source .venv/bin/activate
```

Install dependencies 

```
uv pip install -r requirments.txt
```

Run the agent 

```
python list_tools.py
python k8s-kubectl-ai.py
```
