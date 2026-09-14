# GitHub AI Engineering Assistant

A Streamlit application that reviews public GitHub repositories with Gemini. It combines repository inspection, code review, security review, bug discovery, test generation, change-impact analysis, multilingual reporting, and CSV/DOC export in one workflow.

## Features

- Load source files from a GitHub repository
- Analyze project structure and code quality
- Find likely bugs and security issues
- Inspect the latest commit and estimate change risk
- Run the local pytest suite with a timeout
- Translate the latest report to Thai, Cantonese, Japanese, or Spanish
- Export the latest report as CSV or Word-readable DOC

## Architecture

- `app.py`: Streamlit interface and session state
- `github_service.py`: GitHub API access, file filtering, and repository limits
- `analyzers.py`: Prompt construction for each engineering workflow
- `gemini_service.py`: Gemini client and retry handling
- `report_service.py`: CSV and DOC export helpers
- `test_runner.py`: Bounded local pytest execution
- `tests/`: Regression tests for parsing, reports, translation, and service behavior

## Quick Start

1. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add a Gemini API key.

4. Start the application:

   ```powershell
   streamlit run app.py
   ```

5. Enter a public GitHub repository URL and run an analysis.

## Configuration

`GEMINI_API_KEY` is required. `GITHUB_TOKEN` is optional, but recommended because it increases GitHub API rate limits. `GITHUB_OWNER` and `GITHUB_REPO` are fallback values for non-UI callers.

The GitHub collector limits the number and size of files sent to the model. This helps control latency, token usage, and cost when analyzing larger repositories.

## Testing

Run the test suite from the project directory:

```powershell
$env:PYTHONPATH = (Get-Location).Path
pytest
```

## Interview Talking Points

- External API calls have timeouts and structured error handling.
- Repository input is bounded before it is sent to an LLM.
- AI output is treated as advisory rather than guaranteed truth.
- The application keeps analysis, translation, and export concerns separate.
- Regression tests cover both pure helpers and repaired service behavior.

## Known Limitations

- The application currently targets public GitHub repositories.
- DOC export uses Word-readable HTML with a `.doc` extension; a future version could generate a native `.docx` file.
- AI responses should be reviewed by an engineer before being used as a final code-review decision.
