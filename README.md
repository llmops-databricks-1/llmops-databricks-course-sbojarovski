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
