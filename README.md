# agentic-ecommerce
An ecommerce Agent demonstrating different concepts and features of LangGraph

## Run the agent

**Deploy it to cloud run**
- Run the deploy.sh script
- Do a post request to /invoke
```sh
curl -X POST "[CLOUD_RUN_URL]/invoke" -H "Content-Type: application/json" -d '{
  "messages": ["Recommend me some blue clothing from your catalog for men"],
  "config": {"configurable": {"thread_id": "1"}}
}'
```

## TODO
- [X] Add telemetry for Agent calls
- [X] Create modules to simply imports (nvillaluenga)
- [X] Scripts to deploy web server (cloud run)
- [ ] Create basic chat interface (decide framework)
- [ ] Define set of tools
- [ ] Enable access to Mercado Pago API


## Dependency Management

This project recommends using **uv** for managing dependencies.

**What is uv?**

* uv is a simple and efficient dependency manager for Python projects.
* It focuses on a minimal, declarative approach to defining and installing dependencies.
* uv uses a `uv.toml` file to specify project dependencies, similar to `requirements.txt` but with enhanced features.

**How to use uv:**

1. **Installation:**
   * **macOS and Linux:**
     ```bash
     $ curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   * **Windows:**
     ```powershell
     $ powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

2. **Sync the project**
   ```bash
   uv sync
   ```

3. **Activate the virtual environment**
   ```bash
   . .venv/bin/activate
   ````

Now you are ready to go!

## Telemetry with Langfuse

You can track LLM calls using LangFuse web service or you can deploy it on your
own GCP environment.


### LangFuse Platform

The easiest option is to create a LangFuse account and use their freemium plan. It's very [easy to set up](https://langfuse.com/docs/get-started)

After setting up your account you should complete the following environmental variables:
```bash
LANGFUSE_SECRET_KEY="<add your project's secret key>"
LANGFUSE_PUBLIC_KEY="<add your project's public key>"
LANGFUSE_HOST=https://us.cloud.langfuse.com
```

### Setup on Google Cloud 
[Link to original repository](https://github.com/orgs/langfuse/discussions/4646)

#### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Terraform installed
- Enable the following APIs:
   - Serverless VPC Access API
   - Service Networking API
   - Cloud Run Admin API
   - Cloud Deployment Manager V2 API
   - Artifact Registry API
   - Cloud Identity-Aware Proxy API
   - Cloud Build API
   - Cloud Logging API

#### Getting Started

1. Set your own variables on `terraform.tfvars`
   - Replace the value surrounded by `< >`


2. Terraform init and apply
    ```
    terraform init
    terraform apply
    ```

3. Migrate Terraform state to GCS
    ```
    terraform init -migrate-state
    ```
   - Then generate `backend.tf` and have Terraform state managed by a GCS bucket


4. Access to Langfuse

   - Check your Cloud Run URL on Google Cloud Console (default: `https://langfuse-<your-project-number>.<your-region>.run.app`)
   - Create a project and generate secret & public keys

```bash
LANGFUSE_SECRET_KEY="<add your project's secret key>"
LANGFUSE_PUBLIC_KEY="<add your project's public key>"
LANGFUSE_HOST="https://langfuse-<your-project-number>.<your-region>.run.app"
```