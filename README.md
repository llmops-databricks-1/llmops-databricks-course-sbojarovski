# LLMOps Course on Databricks

## Repo Description

This repository contains the code and assignments for the LLMOps Course on Databricks. It includes:
- Deliverable assignments to be implemented with your own datasets
- Databricks Asset Bundle configurations for deploying to multiple environments
- Automated CI/CD pipelines for testing and validation

To use this repository:
1. Create a feature branch for your work
2. Implement the weekly deliverables
3. Submit a PR to the main branch for review
4. After approval and successful CI pipeline runs, your code will be merged

## Local Development

This project uses Python 3.12 (matching Databricks Serverless Environment 4) and `uv` for dependency management.

### Setup

1. Install `uv` from: https://docs.astral.sh/uv/getting-started/installation/

2. Build the local environment:
   ```bash
   make build
   ```

   Or manually:
   ```bash
   uv sync --extra dev --index https://pypi.org/simple/
   ```

   **Note:** Due to global pypi configuration, you must explicitly specify `--index https://pypi.org/simple/` when running uv commands. The `make build` target handles this automatically.

### Environment Configuration

This project uses Pydantic Settings to manage configuration via environment variables and `.env` files.

**Environment Files:**

Configuration for each deployment target is stored in `./environments/`:

| File | Purpose |
|------|---------|
| `environments/local.env` | Local development |
| `environments/dev.env` | Development Databricks target |
| `environments/prod.env` | Production Databricks target |
| `environments/cauchy.env` | Cauchy Databricks target |

**PyCharm Setup:**

To automatically load environment variables when running code in PyCharm:

1. Open **Run → Edit Configurations**
2. Select your run configuration (or create a new one)
3. Under **Environment**, click the folder icon
4. Select `environments/local.env` to load local configuration
5. Click **OK**

Alternatively, you can set the environment file for all run configurations via **PyCharm → Settings → Tools → Python Integrated Tools → Default test runner** and configuring the environment there.

**Configuration Structure:**

The Settings class includes:
- `spark_session_profile` — Profile name for Databricks Connect
- `databricks.host` — Databricks workspace URL (from `databricks.yml` targets)
- `databricks.serverless_compute_id` — Optional serverless compute ID

**Using Settings in Code:**

```python
from llmops_databricks_course_sbojarovski.config import get_settings

# Load settings for local environment
settings = get_settings(environment="local")
print(settings.spark_session_profile)  # "bojarovski-llmops"
print(settings.databricks.host)  # "https://dbc-749ee571-055f.cloud.databricks.com"
print(settings.databricks.serverless_compute_id)  # None

# Override with environment variables (use double underscore for nested fields)
import os
os.environ["SPARK_SESSION_PROFILE"] = "custom-profile"
os.environ["DATABRICKS__SERVERLESS_COMPUTE_ID"] = "compute-123"
settings = get_settings(environment="local")
print(settings.spark_session_profile)  # "custom-profile"
print(settings.databricks.serverless_compute_id)  # "compute-123"
```

**Environment Variable Format:**

For nested Databricks configuration, use double underscore:
```bash
# Set Databricks host
export DATABRICKS__HOST=https://custom.cloud.databricks.com

# Set serverless compute ID
export DATABRICKS__SERVERLESS_COMPUTE_ID=my-compute-id

# Or in .env file
DATABRICKS__HOST=https://custom.cloud.databricks.com
DATABRICKS__SERVERLESS_COMPUTE_ID=my-compute-id
```

**Workspace Hosts by Target:**

Each target has its workspace host configured:
- `local`, `dev`, `prod`: `https://dbc-749ee571-055f.cloud.databricks.com` (shared workspace)
- `cauchy`: `https://dbc-b1b2f91a-d102.cloud.databricks.com` (separate workspace for Unity Catalog)
- Default (free tier): `https://community.cloud.databricks.com`

**In Notebooks:**

When running notebooks on Databricks, environment variables can be set at the cluster level or passed via `databricks.yml` configuration. The CI/CD pipeline injects secrets as environment variables during deployment.

### Common Commands

Use the Makefile for convenient development workflows:

```bash
# Build the environment
make build

# Run linting and code formatting checks
make lint

# Run tests
make test

# Deploy to Databricks local target
make deploy

# Show all available commands
make help
```

All `make` targets automatically handle the PyPI index configuration, so you don't need to specify it manually.

## Deployment

### Deployment Targets

The project is configured with the following Databricks deployment targets in `databricks.yml`:

| Target | Mode | Use Case                                                                 |
|--------|------|--------------------------------------------------------------------------|
| `local` | Development | Local development and testing                                            |
| `dev` | Development | Development / Staging environment                                        |
| `prod` | Production | Production environment                                                   |
| `cauchy` | Development | Used for features not available in the Databricks Free Edition Workspace |

- **Development targets** (`local`, `dev`) are used for active development and testing
- **Production target** (`prod`) is reserved for production deployments via CI/CD pipelines
- **Cauchy target** is used for testing features that are not available in the Databricks Free Edition Workspace,
  such as Unity Catalog and Serverless SQL Endpoints. This allows to run certain features in the course while using the
  Free Edition for the majority of the work.
- The `local` target is the default for manual deployments

### Deploying to Local Target

Deploy to the local target using:

```bash
make deploy
```

This will:
1. **Validate** the bundle configuration
2. **Build** the project wheel with PyPI package index
3. **Deploy** to Databricks
4. **Summarize** the deployment

Alternatively, run commands individually:
```bash
# Validate
databricks --profile bojarovski-llmops bundle validate --target=local

# Deploy
databricks --profile bojarovski-llmops bundle deploy --target=local

# View summary
databricks --profile bojarovski-llmops bundle summary --target=local
```

### CI/CD Deployments

The `dev` and `prod` targets are deployed automatically via GitHub Actions when code is merged to main. GitHub Actions workflows use Databricks OAuth credentials configured as repository secrets.

To set up CI/CD credentials:
```bash
# Dev environment
gh secret set DATABRICKS_DEV_CLIENT_ID --body "57f73d1d-3240-4316-9371-bc91e010a7fb"
gh secret set DATABRICKS_DEV_CLIENT_SECRET --body "<dev-client-secret-here>"

# Prod environment
gh secret set DATABRICKS_PROD_CLIENT_ID --body "445fb0db-33fb-419e-af20-af280dadb9c4"
gh secret set DATABRICKS_PROD_CLIENT_SECRET --body "<prod-client-secret-here>"
```
