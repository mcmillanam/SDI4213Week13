# SDI 4213 Week 13 — Kubernetes Individual Exercise

## Help Desk on Kubernetes

This starter repository contains a small browser-based Help Desk application and partially completed Kubernetes manifests. Your job is to deploy the application and PostgreSQL to **Minikube**, verify persistence and health, scale the application, and demonstrate Kubernetes self-healing.

### Architecture

Browser → Help Desk Service → Help Desk Pods (2+) → PostgreSQL Service → PostgreSQL Pod → PVC

### Important

- Do **not** commit a real password or a generated Kubernetes Secret manifest containing the actual password.
- The provided `k8s/secret-template.yaml` is a template only and is intentionally excluded from `kustomization.yaml`.
- Create the real Secret locally with `kubectl create secret ...` as described in the assignment.

### Quick local test

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
```

See `docs/Week13_Individual_Exercise.docx` for the full assignment.
