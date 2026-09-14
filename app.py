import re

import streamlit as st

from analyzers import (
    analyze_change_impact,
    analyze_project,
    analyze_test_failure,
    code_review,
    find_bugs,
    generate_test_cases,
    security_scan,
    translate_report,
)
from github_service import (
    collect_repository_code,
    get_changed_files_from_latest_commit,
)
from report_service import report_as_csv, report_as_doc
from test_runner import run_tests


def parse_github_url(url):
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url.strip())

    if not match:
        return None, None

    owner = match.group(1)
    repo = match.group(2)

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def extract_score(text, pattern):
    if not text or not isinstance(text, str):
        return None

    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def extract_risk_level(text):
    if not text or not isinstance(text, str):
        return None

    match = re.search(
        r"OVERALL RISK LEVEL:\s*(LOW|MEDIUM|HIGH|CRITICAL)",
        text,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).upper()
    return None


st.set_page_config(
    page_title="GitHub AI Engineering Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("GitHub AI Engineering Assistant")
st.write("AI-assisted code review, testing, and change impact analysis.")

st.subheader("Repository")
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
)

if "owner" not in st.session_state:
    st.session_state.owner = None
if "repo" not in st.session_state:
    st.session_state.repo = None
if "project_context" not in st.session_state:
    st.session_state.project_context = None
if "files" not in st.session_state:
    st.session_state.files = None
if "code_score" not in st.session_state:
    st.session_state.code_score = None
if "security_score" not in st.session_state:
    st.session_state.security_score = None
if "risk_score" not in st.session_state:
    st.session_state.risk_score = None
if "risk_level" not in st.session_state:
    st.session_state.risk_level = None
if "test_passed" not in st.session_state:
    st.session_state.test_passed = None
if "test_failed" not in st.session_state:
    st.session_state.test_failed = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_report_type" not in st.session_state:
    st.session_state.last_report_type = None
if "translated_result" not in st.session_state:
    st.session_state.translated_result = None
if "translated_language" not in st.session_state:
    st.session_state.translated_language = None


def store_result(result, report_type):
    st.session_state.last_result = result
    st.session_state.last_report_type = report_type
    st.session_state.translated_result = None
    st.session_state.translated_language = None

st.subheader("Engineering Dashboard")
col1, col2, col3, col4 = st.columns(4)

with col1:
    code_value = (
        f"{st.session_state.code_score}/100"
        if st.session_state.code_score is not None
        else "-"
    )
    st.metric("Code Quality", code_value)

with col2:
    security_value = (
        f"{st.session_state.security_score}/100"
        if st.session_state.security_score is not None
        else "-"
    )
    st.metric("Secure Coding", security_value)

with col3:
    if st.session_state.risk_score is not None:
        risk_value = (
            f"{st.session_state.risk_score}/10 {st.session_state.risk_level or ''}"
        )
    else:
        risk_value = "-"
    st.metric("Change Risk", risk_value)

with col4:
    if st.session_state.test_passed is not None:
        test_value = f"{st.session_state.test_passed} Passed"
        if st.session_state.test_failed:
            test_value += f" / {st.session_state.test_failed} Failed"
    else:
        test_value = "-"
    st.metric("Automated Tests", test_value)

if st.button("Load Repository"):
    if not repo_url.strip():
        st.warning("Please enter a GitHub repository URL.")
    else:
        owner, repo = parse_github_url(repo_url)

        if not owner or not repo:
            st.error("Use a valid GitHub URL like https://github.com/username/repository")
        else:
            st.session_state.owner = owner
            st.session_state.repo = repo

            with st.spinner("Loading repository..."):
                files = collect_repository_code(owner, repo)

            if not files:
                st.error("No source files found.")
            else:
                project_context = ""
                for file in files:
                    project_context += f"""
========================================
FILE: {file['path']}
========================================

{file['code']}

"""

                st.session_state.files = files
                st.session_state.project_context = project_context
                st.success(f"Loaded {len(files)} source files.")

if st.session_state.project_context:
    st.success("Repository is ready for analysis.")
    st.write(f"Source files loaded: {len(st.session_state.files)}")
    st.divider()
    st.subheader("AI Analysis")

    if st.button("Analyze Project"):
        with st.spinner("Analyzing project..."):
            result = analyze_project(st.session_state.project_context)
        st.markdown(result)
        store_result(result, "project_analysis")

    if st.button("AI Code Review"):
        with st.spinner("Running code review..."):
            result = code_review(st.session_state.project_context)
        st.markdown(result)
        st.session_state.code_score = extract_score(result, r"CODE REVIEW SCORE:\s*(\d+)")
        store_result(result, "code_review")

    if st.button("Find Possible Bugs"):
        with st.spinner("Searching for possible bugs..."):
            result = find_bugs(st.session_state.project_context)
        st.markdown(result)
        store_result(result, "bug_finding")

    if st.button("Secure Coding Review"):
        with st.spinner("Reviewing secure coding practices..."):
            result = security_scan(st.session_state.project_context)
        st.markdown(result)
        st.session_state.security_score = extract_score(
            result,
            r"SECURE CODING SCORE:\s*(\d+)",
        )
        store_result(result, "security_review")

    if st.button("Generate Test Cases"):
        with st.spinner("Generating test cases..."):
            result = generate_test_cases(st.session_state.project_context)
        st.markdown(result)
        store_result(result, "test_cases")

    if st.button("Change Impact Analysis"):
        with st.spinner("Checking latest GitHub commit..."):
            changed_files = get_changed_files_from_latest_commit(
                st.session_state.owner,
                st.session_state.repo,
            )

        if not changed_files:
            st.warning("No changed files found.")
        else:
            st.subheader("Latest Changed Files")
            for file in changed_files:
                st.write(
                    f"{file['filename']} | {file['status']} | +{file['additions']} -{file['deletions']}"
                )

            with st.spinner("Analyzing change impact..."):
                result = analyze_change_impact(
                    changed_files,
                    st.session_state.project_context,
                )
            st.markdown(result)
            st.session_state.risk_score = extract_score(result, r"RISK SCORE:\s*(\d+)")
            st.session_state.risk_level = extract_risk_level(result)
            store_result(result, "change_impact")

    if st.button("Run Automated Tests"):
        with st.spinner("Running pytest..."):
            return_code, test_output = run_tests()

        st.code(test_output, language="text")

        if return_code == 0:
            st.success("All tests PASSED.")
        else:
            st.error("Some tests FAILED.")

        with st.spinner("AI is analyzing test failure..."):
            analysis = analyze_test_failure(
                test_output,
                st.session_state.project_context,
            )

        st.subheader("AI Failure Analysis")
        st.markdown(analysis)

        passed_match = re.search(r"(\d+)\s+passed", test_output, re.IGNORECASE)
        failed_match = re.search(r"(\d+)\s+failed", test_output, re.IGNORECASE)

        st.session_state.test_passed = int(passed_match.group(1)) if passed_match else 0
        st.session_state.test_failed = int(failed_match.group(1)) if failed_match else 0
        store_result(analysis, "test_failure")

    if st.session_state.last_result:
        st.divider()
        st.subheader("Translate and Export Latest Report")
        report_name = st.session_state.last_report_type or "analysis"
        repository = f"{st.session_state.owner}/{st.session_state.repo}"
        language_col, translate_col = st.columns([2, 1])

        with language_col:
            selected_language = st.selectbox(
                "Translate report to",
                ["Original", "Thai", "Cantonese", "Japanese", "Spanish"],
            )

        with translate_col:
            st.write("")
            if st.button("Translate Report", use_container_width=True):
                if selected_language == "Original":
                    st.session_state.translated_result = None
                    st.session_state.translated_language = None
                else:
                    with st.spinner(f"Translating to {selected_language}..."):
                        st.session_state.translated_result = translate_report(
                            st.session_state.last_result,
                            selected_language,
                        )
                    st.session_state.translated_language = selected_language

        report_content = (
            st.session_state.translated_result
            or st.session_state.last_result
        )
        if st.session_state.translated_result:
            st.subheader(f"{st.session_state.translated_language} Translation")
            st.markdown(st.session_state.translated_result)

        export_name = report_name
        if st.session_state.translated_language:
            export_name = f"{report_name}_{st.session_state.translated_language.lower()}"

        export_col1, export_col2 = st.columns(2)

        with export_col1:
            st.download_button(
                "Download CSV",
                data=report_as_csv(
                    export_name,
                    report_content,
                    repository,
                ),
                file_name=f"{export_name}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with export_col2:
            st.download_button(
                "Download DOC",
                data=report_as_doc(
                    export_name,
                    report_content,
                    repository,
                ),
                file_name=f"{export_name}.doc",
                mime="application/msword",
                use_container_width=True,
            )
