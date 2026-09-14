import subprocess
import sys


def run_tests(timeout=120):

    command = [sys.executable, "-m", "pytest", "-v"]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        return 124, f"Test run timed out after {timeout} seconds.\n{output}"

    output = result.stdout

    if result.stderr:
        output += "\n" + result.stderr

    return result.returncode, output