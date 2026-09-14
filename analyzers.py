from gemini_service_Time import ask_ai

TRANSLATION_LANGUAGES = {
    "Thai": "Thai",
    "Cantonese": "Cantonese written in Traditional Chinese characters",
    "Japanese": "Japanese",
    "Spanish": "Spanish",
}


def translate_report(report, language):
    """Translate a report while preserving its headings and formatting."""
    target_language = TRANSLATION_LANGUAGES.get(language)
    if not target_language:
        raise ValueError("Unsupported translation language.")

    prompt = f"""
Translate the following software engineering report into {target_language}.

Preserve the original headings, lists, code snippets, scores, filenames,
identifiers, and technical meaning. Translate explanatory prose only.
Return only the translated report, with no introduction or commentary.

REPORT:
{report}
"""
    return ask_ai(prompt)


# =========================================
# 1. ANALYZE PROJECT
# =========================================

def analyze_project(project_context):

    prompt = f"""
You are a senior software engineer.

Analyze the following GitHub repository.

Explain:

1. What this project does
2. Main features
3. Important files
4. How the files work together
5. Strengths
6. Areas for improvement

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =========================================
# 2. CODE REVIEW
# =========================================

def code_review(project_context):

    prompt = f"""
You are a senior software engineer.

Perform a professional code review
of the following repository.

Return:

CODE REVIEW SCORE: XX/100

SUMMARY:

CRITICAL ISSUES:

WARNINGS:

CODE QUALITY:

BEST PRACTICES:

RECOMMENDED IMPROVEMENTS:

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =========================================
# 3. FIND POSSIBLE BUGS
# =========================================

def find_bugs(project_context):

    prompt = f"""
You are a software QA engineer.

Analyze this repository and identify
possible software defects.

For each issue return:

BUG ID:
SEVERITY:
FILE:
PROBLEM:
WHY IT MAY FAIL:
SUGGESTED FIX:

Also return:

OVERALL RISK SCORE: X/10

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =========================================
# 4. SECURE CODING REVIEW
# =========================================

def security_scan(project_context):

    prompt = f"""
You are reviewing your own software project
for defensive secure coding.

Do not provide exploitation instructions.

Check for:

- Hard-coded credentials
- Sensitive information exposure
- Missing input validation
- Unsafe exception handling
- API error handling
- Secret management
- Configuration problems

Return:

SECURE CODING SCORE: XX/100

GOOD PRACTICES:

ISSUES FOUND:

SEVERITY:
FILE:
PROBLEM:
WHY IT MATTERS:
SAFE RECOMMENDATION:

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =========================================
# 5. GENERATE TEST CASES
# =========================================

def generate_test_cases(project_context):

    prompt = f"""
You are a professional software QA engineer.

Generate practical test cases
for this software project.

For each test return:

TEST CASE ID:
FEATURE:
TEST SCENARIO:
TEST TYPE:
PRECONDITION:
TEST STEPS:
INPUT:
EXPECTED RESULT:
PRIORITY:

Include:

- Positive tests
- Negative tests
- Boundary tests
- Edge cases
- Error handling tests

Repository:

{project_context}
"""

    return ask_ai(prompt)


# =========================================
# 7. CHANGE IMPACT ANALYSIS
# =========================================

def analyze_change_impact(changed_files, project_context):

    if not changed_files:
        return "No changed files found."

    change_text = ""

    for file in changed_files:

        change_text += f"""
========================================
FILE: {file['filename']}
STATUS: {file['status']}
ADDITIONS: {file['additions']}
DELETIONS: {file['deletions']}
TOTAL CHANGES: {file['changes']}

CODE CHANGES:
{file['patch']}
========================================
"""

    prompt = f"""
You are a senior software engineer
and QA engineer.

Analyze the latest changes
in this GitHub repository.

Determine how the code changes
may affect the existing system.

Return the result using this format:

CHANGE SUMMARY:
Explain what was changed.

OVERALL RISK LEVEL:
LOW / MEDIUM / HIGH / CRITICAL

RISK SCORE:
X/10

AFFECTED AREAS:
List features or modules
that may be affected.

POSSIBLE SIDE EFFECTS:
Explain what existing functionality
may be affected.

REGRESSION RISK:
Explain what should be tested again.

RECOMMENDED REGRESSION TESTS:

TEST 1
FEATURE:
SCENARIO:
PRIORITY:
EXPECTED RESULT:

TEST 2
FEATURE:
SCENARIO:
PRIORITY:
EXPECTED RESULT:

MANUAL CHECKS:
List anything that should be
manually verified.

Do not invent functionality
that does not exist in the repository.

LATEST CODE CHANGES:

{change_text}

CURRENT PROJECT:

{project_context}
"""

    return ask_ai(prompt)

# =========================================
# TEST FAILURE ANALYSIS
# =========================================

def analyze_test_failure(test_output, project_context):

    prompt = f"""
You are a software QA engineer and developer.

An automated test has failed.

Analyze the test result and help the developer
understand the possible cause.

Return the result using this format:

FAILURE SUMMARY:
Explain what failed.

POSSIBLE ROOT CAUSE:
Explain the most likely cause.

RELATED AREA:
Identify the file, function, or module that may be related.

SEVERITY:
LOW / MEDIUM / HIGH / CRITICAL

RECOMMENDED INVESTIGATION:
Explain what the developer should check.

SUGGESTED FIX:
Provide a safe suggested solution.

RETEST RECOMMENDATION:
Explain which tests should be run again after fixing the issue.

Important:
Do not assume the AI analysis is guaranteed correct.
Base the analysis on the available test output and repository context.

AUTOMATED TEST OUTPUT:

{test_output}

PROJECT SOURCE CODE:

{project_context}
"""
    
    return ask_ai(prompt)