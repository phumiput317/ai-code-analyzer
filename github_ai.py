import os
import base64
import requests
from datetime import datetime

from dotenv import load_dotenv
from google import genai

# =============================
# CONFIG
# =============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit()

client = genai.Client(api_key=API_KEY)

OWNER = "phumiput317"
REPO = "HW03-65123317"

MODEL = "gemini-3.6-flash"


# =============================
# GET FILES FROM GITHUB
# =============================

def get_repository_files(path=""):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"

    response = requests.get(url)

    if response.status_code != 200:
        print("ERROR: Cannot access GitHub repository")
        print(response.text)
        return []

    return response.json()


# =============================
# READ FILE
# =============================

def read_github_file(file_info):
    try:
        content = base64.b64decode(file_info["content"]).decode(
            "utf-8",
            errors="ignore"
        )
        return content
    except Exception as e:
        print("Cannot read file:", e)
        return ""


# =============================
# COLLECT SOURCE CODE
# =============================

def collect_repository_code(path=""):
    allowed_extensions = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".json",
        ".html",
        ".css"
    )

    collected = []

    files = get_repository_files(path)

    for item in files:

        # Folder
        if item["type"] == "dir":
            collected.extend(
                collect_repository_code(item["path"])
            )

        # File
        elif item["type"] == "file":

            if item["name"].endswith(allowed_extensions):

                print(f"Reading: {item['path']}")

                file_url = item["url"]

                response = requests.get(file_url)

                if response.status_code == 200:
                    file_data = response.json()

                    code = read_github_file(file_data)

                    if code:
                        collected.append(
                            {
                                "path": item["path"],
                                "code": code
                            }
                        )

    return collected


# =============================
# BUILD PROJECT CONTEXT
# =============================

def build_project_context(files):

    context = ""

    for file in files:

        context += f"""

========================================
FILE: {file['path']}
========================================

{file['code']}

"""

    return context


# =============================
# ASK GEMINI
# =============================

def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI ERROR: {e}"


# =============================
# PROJECT ANALYSIS
# =============================

def analyze_project(project_context):

    prompt = f"""
You are a senior software engineer.

Analyze this GitHub repository.

Explain:

1. What this project does
2. Main features
3. Main programming languages
4. Important files
5. How the files work together
6. Strengths of the project
7. Areas that should be improved

Use clear and concise language.

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =============================
# AI CODE REVIEW
# =============================

def code_review(project_context):

    prompt = f"""
You are a senior software engineer performing a professional code review.

Review the following GitHub repository.

Return the result using this format:

CODE REVIEW SCORE: XX/100

SUMMARY:
Short overview of code quality.

CRITICAL ISSUES:
- file
- issue
- reason
- recommended fix

WARNINGS:
- file
- issue
- recommended fix

CODE QUALITY:
Explain readability, maintainability, structure and naming.

SECURITY:
Identify security risks such as:
- hard coded API keys
- passwords
- unsafe input
- insecure API calls
- exposed secrets

BEST PRACTICES:
Suggest improvements.

Repository source code:

{project_context}
"""

    return ask_ai(prompt)


# =============================
# BUG FINDER
# =============================

def find_bugs(project_context):

    prompt = f"""
You are a senior QA engineer and software developer.

Analyze the following source code and identify possible software bugs.

For every issue return:

BUG ID:
SEVERITY: Critical / High / Medium / Low
FILE:
PROBLEM:
WHY IT MAY FAIL:
HOW TO REPRODUCE:
SUGGESTED FIX:

Also provide:

OVERALL RISK SCORE: X/10

Focus on:

- runtime errors
- incorrect conditions
- missing validation
- exception handling
- API failures
- null values
- edge cases
- security problems
- performance problems

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =============================
# TEST CASE GENERATOR
# =============================

def generate_test_cases(project_context):

    prompt = f"""
You are a professional software QA engineer.

Analyze the following project and generate practical software test cases.

Include:

TEST CASE ID
FEATURE
TEST SCENARIO
TEST TYPE
PRECONDITION
TEST STEPS
INPUT
EXPECTED RESULT
PRIORITY

Generate:

- Positive tests
- Negative tests
- Boundary tests
- Edge cases
- API failure tests
- Security related tests

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =============================
# SECURITY SCAN
# =============================

def security_scan(project_context):

    prompt = f"""
You are reviewing your own software project for defensive
secure coding and code quality.

This is NOT a penetration test.
Do NOT provide exploitation instructions.

Review the source code only for common defensive
software-development mistakes.

Check for:

1. API keys, passwords or tokens accidentally stored in source code
2. Missing use of environment variables for credentials
3. Sensitive information printed in logs
4. Missing input validation
5. Unsafe exception handling
6. Missing error handling for external APIs
7. Configuration files that should not be committed
8. .env and secret-management best practices
9. Dependency and configuration hygiene
10. General secure-coding improvements

Return the result in this format:

SECURE CODING SCORE: XX/100

GOOD PRACTICES:
- ...

ISSUES FOUND:

ISSUE 1
FILE:
SEVERITY: High / Medium / Low
PROBLEM:
WHY IT MATTERS:
SAFE RECOMMENDATION:

ISSUE 2
...

RECOMMENDED IMPROVEMENTS:
- ...

Do not explain how to exploit any issue.
Only provide defensive recommendations.

Repository source code:

{project_context}
"""

    return ask_ai(prompt)

# =============================
# INTERACTIVE AI
# =============================

def chat_with_repository(project_context):

    last_question = None
    last_answer = None
    file_name = "repository_analysis"

    print("\nRepository AI Chat")
    print("Type 'back' to return to menu.")
    print("/menu  = AI functions")
    print("/file  = change file")
    print("/save  = save latest AI report")
    print("/clear = clear conversation")
    print("/exit  = exit program")

    while True:

        question = input("\nAsk AI: ")

        if question.lower() == "back":
            break

        if question.lower() == "/menu":
            print("/menu  = AI functions")
            print("/file  = change file")
            print("/save  = save latest AI report")
            print("/clear = clear conversation")
            print("/exit  = exit program")
            continue

        if question.lower() == "/save":
            if not last_answer:
                print("\nNo AI analysis available to save.")
                continue

            save_report(
                file_name,
                last_question,
                last_answer
            )
            continue

        if question.lower() == "/clear":
            last_question = None
            last_answer = None
            print("\nConversation cleared.")
            continue

        if question.lower() == "/exit":
            print("\nExiting AI chat.")
            break

        if question.lower() == "/file":
            print("\nChange file feature is not implemented yet.")
            continue

        prompt = f"""
You are an AI software engineering assistant.

Answer questions based only on the following repository.

Repository:

{project_context}

User Question:

{question}
"""

        result = ask_ai(prompt)

        last_question = question
        last_answer = result

        print("\nAI:")
        print(result)

###Get Recent Commits###

def get_recent_commits():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Cannot get commits:", e)
        return []

###Detect Changed Files###

def get_changed_files_from_latest_commit():
    commits = get_recent_commits()

    if not commits:
        return []

    latest_sha = commits[0]["sha"]

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits/{latest_sha}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        changed_files = []

        for file in data.get("files", []):
            changed_files.append({
                "filename": file.get("filename"),
                "status": file.get("status"),
                "additions": file.get("additions"),
                "deletions": file.get("deletions"),
                "changes": file.get("changes"),
                "patch": file.get("patch", "")
            })

        return changed_files

    except Exception as e:
        print("Cannot get changed files:", e)
        return []

### AI Change Impact Analysis ###

def analyze_change_impact(changed_files, project_context):

    if not changed_files:
        return "No changed files found."

    change_text = ""

    for file in changed_files:
        change_text += f"""
FILE: {file['filename']}
STATUS: {file['status']}
ADDITIONS: {file['additions']}
DELETIONS: {file['deletions']}
TOTAL CHANGES: {file['changes']}

PATCH:
{file['patch']}

----------------------------------------
"""

    prompt = f"""
You are a senior software engineer and QA engineer.

Analyze the latest GitHub code changes.

Your goal is to determine the impact of these changes
on the existing software system.

Return the result in this format:

CHANGE SUMMARY:
Explain what changed.

OVERALL RISK LEVEL:
LOW / MEDIUM / HIGH / CRITICAL

RISK SCORE:
X/10

CHANGED FILES:
List each changed file and explain the purpose of the change.

POSSIBLE IMPACT:
- Feature affected
- Module affected
- Possible side effects
- Dependencies affected

REGRESSION RISK:
Explain what existing functionality could break.

RECOMMENDED REGRESSION TESTS:

TEST 1
FEATURE:
SCENARIO:
PRIORITY:
EXPECTED RESULT:

TEST 2
...

MANUAL CHECKS:
List important things a developer or tester should verify manually.

Do not invent features that are not supported by the repository.

LATEST CHANGES:

{change_text}

CURRENT REPOSITORY:

{project_context}
"""

    return ask_ai(prompt)

def show_latest_changes():

    print("\nChecking latest GitHub commit...\n")

    changed_files = get_changed_files_from_latest_commit()

    if not changed_files:
        print("No changed files found.")
        return []

    print("Latest Changed Files")
    print("--------------------")

    for file in changed_files:

        print(
            f"{file['filename']} | "
            f"{file['status']} | "
            f"+{file['additions']} "
            f"-{file['deletions']}"
        )

    return changed_files

# =============================
# MENU
# =============================

def show_menu():

    print("""
=========================================
       GitHub AI Engineering Assistant
=========================================

1. Analyze Project
2. AI Code Review
3. Find Possible Bugs
4. Secure Coding Review
5. Generate Test Cases
6. Ask AI About Repository
7. Git Change Impact Analysis
8. Exit

=========================================
""")


# =============================
# MAIN
# =============================

def main():

    print("\nConnecting to GitHub...")
    print(f"Repository: {OWNER}/{REPO}")

    files = collect_repository_code()

    if not files:
        print("No supported source files found.")
        return

    print(f"\nLoaded {len(files)} source files.")

    project_context = build_project_context(files)

    while True:

        show_menu()

        choice = input("Select: ")

        if choice == "1":
            print("\nAnalyzing project...\n")
            result = analyze_project(project_context)
            print(result)

        elif choice == "2":
            print("\nRunning AI Code Review...\n")
            result = code_review(project_context)
            print(result)


        elif choice == "3":
            print("\nSearching for possible bugs...\n")
            result = find_bugs(project_context)
            print(result)


        elif choice == "4":
            print("\nRunning Security Scan...\n")
            result = security_scan(project_context)
            print(result)

        elif choice == "5":
            print("\nGenerating Test Cases...\n")
            result = generate_test_cases(project_context)
            print(result)

        elif choice == "6":
            chat_with_repository(project_context)

        elif choice == "7":
            print("\nRunning Git Change Impact Analysis...\n")
            changed_files = show_latest_changes()

            if changed_files:
                print("\nAnalyzing impact with AI...\n")
                result = analyze_change_impact(
                    changed_files,
                    project_context
                )
            print(result)

        elif choice == "8":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid menu selection.")


if __name__ == "__main__":
    main()