from test_runner import run_tests
from config import OWNER, REPO
from report_service import save_report
from github_service import (
    collect_repository_code
)

from analyzers import (
    analyze_project,
    code_review,
    find_bugs,
    security_scan,
    generate_test_cases,
    analyze_test_failure,
    analyze_change_impact
)


def build_project_context(
    files
):

    context = ""

    for file in files:

        context += f"""

========================
FILE: {file['path']}
========================

{file['code']}

"""

    return context


def show_menu():

    print("""
==================================
 GitHub AI Engineering Assistant
==================================

1. Analyze Project
2. AI Code Review
3. Find Bugs
4. Secure Coding Review
5. Generate Test Cases
6. Change Impact Analysis
7. Export Report
8. Run Automated Tests
9. Exit

==================================
""")


def main():

    print(
        f"Repository: "
        f"{OWNER}/{REPO}"
    )

    files = (
        collect_repository_code(OWNER, REPO)
    )

    if not files:

        print(
            "No source files found."
        )

        return

    project_context = (
        build_project_context(
            files
        )
    )

    while True:

        show_menu()

        choice = input(
            "Select: "
        )

        if choice == "1":

            result = (
                analyze_project(
                    project_context
                )
            )

            print(result)

        elif choice == "2":

            result = (
                code_review(
                    project_context
                )
            )

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

            print("\nChecking latest GitHub changes...\n")

            changed_files = get_changed_files_from_latest_commit()

            if not changed_files:
                print("No changed files found.")
            continue

            print("Latest Changed Files")
            print("=" * 50)

            for file in changed_files:
                print(
                f"{file['filename']} | "
                f"{file['status']} | "
                f"+{file['additions']} "
                f"-{file['deletions']}"
            )

            print("\nAnalyzing change impact with AI...\n")

            result = analyze_change_impact(
            changed_files,
            project_context
            )

            print(result)

        elif choice == "7":

            print("\nExport Report\n")

            result = code_review(project_context)

            filename = save_report(
                "code_review",
            result
        )

            print(f"\nReport saved successfully:")
            print(filename) 

        elif choice == "8":

            print("\nRunning Automated Tests...\n")

            return_code, test_output = run_tests()

            print(test_output)

            if return_code == 0:

                print("\nAll tests PASSED.")

            else:

                print("\nSome tests FAILED.")

                print("\nAnalyzing test failure with AI...\n")

                analysis = analyze_test_failure(
                    test_output,
                    project_context
                )

                print(analysis)

        elif choice == "9":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid menu selection.")


if __name__ == "__main__":
    main()
import subprocess


