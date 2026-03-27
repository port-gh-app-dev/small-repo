# small-repo

A small Python project that demonstrates a simple application and provides [Port.io](https://www.getport.io/) GitOps integration utilities.

## Overview

This repository contains:

- **`main.py`** – A minimal Python entry point that prints a greeting.
- **`port-gitops.py`** – A utility script that reads a single Port.io entity document from `port.yml` and expands it into 5,000 uniquely-identified documents (useful for bulk-loading test data into Port).
- **`port.yml`** – Port.io entity definitions managed via GitOps.
- **`single.yml`** – A single Port.io entity template.
- **GitHub Actions workflows** – Automated pipelines for code quality, Port.io Kafka integration, and GitHub custom-property synchronisation.

## Prerequisites

- [Python](https://www.python.org/downloads/) **≥ 3.12**
- [uv](https://github.com/astral-sh/uv) (recommended) **or** `pip`

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/port-gh-app-dev/small-repo.git
cd small-repo
```

### 2. Install dependencies

Using **uv** (recommended):

```bash
uv sync
```

Using **pip**:

```bash
pip install -e .
```

### 3. Run the application

```bash
python main.py
```

Expected output:

```
Hello from small-repo!
```

## Scripts

### `port-gitops.py` – Bulk Port.io entity generator

Reads the first YAML document from `port.yml` as a template and writes 5,000 documents back to the file, each with a unique `identifier` suffix (`<original-identifier>-1` … `<original-identifier>-5000`).

```bash
python port-gitops.py
```

> **Note:** This script overwrites `port.yml` in place. Make sure you have a backup or are working in a clean Git branch before running it.

## Project Structure

```
small-repo/
├── .github/
│   └── workflows/
│       ├── build.yaml                 # SonarQube code-quality scan
│       ├── port-kafka.yaml            # Port.io Kafka integration
│       └── sync_custom_properties.yaml # Sync GitHub custom properties to Port
├── main.py                            # Application entry point
├── port-gitops.py                     # Port.io bulk entity generator
├── port.yml                           # Port.io entity definitions (GitOps)
├── single.yml                         # Single Port.io entity template
├── pyproject.toml                     # Python project metadata & dependencies
├── sonar-project.properties           # SonarQube project configuration
└── README.md
```

## CI/CD Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **Build** (`build.yaml`) | Push to `main`, Pull Request | SonarQube static analysis |
| **Kafka Exporter** (`port-kafka.yaml`) | Push to `main`, Manual | Port.io Kafka integration via Ocean |
| **Sync Custom Properties** (`sync_custom_properties.yaml`) | Manual | Sync GitHub repository custom properties to Port scorecards |

## Required Secrets

| Secret | Used by |
|--------|---------|
| `SONAR_TOKEN` | SonarQube scan |
| `PORT_CLIENT_ID` / `PORT_CLIENT_SECRET` | Port.io GitHub Actions |
| `OCEAN__PORT__CLIENT_ID` / `OCEAN__PORT__CLIENT_SECRET` | Port.io Kafka exporter |
| `OCEAN__INTEGRATION__CONFIG__CLUSTER_CONF_MAPPING` | Port.io Kafka exporter |
| `PORT_GITHUB_APP_PEM` / `PORT_GITHUB_APP_ID` / `PORT_GITHUB_APP_INSTALLATION_ID` | Custom-property sync |

## Dependencies

| Package | Version |
|---------|---------|
| [PyYAML](https://pyyaml.org/) | `>=6.0.2` |

## License

This project is provided as-is for demonstration purposes.
