# agentic-ecommerce
An ecommerce Agent demonstrating different concepts and features of LangGraph

## TODO
- [ ] Add telemetry for Agent calls
- [X] Create modules to simply imports
- [ ] Scripts to deploy web server (cloud run)
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
