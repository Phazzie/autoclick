"""Code quality checker tool"""
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class QualityCheck:
    """Represents a code quality check configuration"""

    command: List[str]
    name: str
    description: str


def run_command(command: List[str]) -> Tuple[int, str]:
    """Run a command and return exit code and output"""
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode, result.stdout
    except Exception as e:
        return 1, str(e)


def check_code_quality() -> bool:
    """Run code quality checks"""
    project_root = Path(__file__).parent.parent
    print(f"Checking code quality in: {project_root}")

    checks = [
        # KISS - Check function/class sizes
        QualityCheck(
            command=[
                "pylint",
                "src",
                "tests",
                "--max-line-length=100",
                "--max-args=3",
                "--max-locals=5",
                "--max-statements=10",
                "--disable=astroid-error,import-error,ungrouped-imports,missing-module-docstring",
            ],
            name="KISS checks",
            description="Checking for code simplicity (KISS principle)",
        ),
        # SOLID - Check class responsibilities
        QualityCheck(
            command=[
                "pylint",
                "src",
                "tests",
                "--max-public-methods=5",
                "--min-public-methods=1",
                "--max-parents=2",
                "--disable=astroid-error,import-error,ungrouped-imports,missing-module-docstring",
            ],
            name="SOLID checks",
            description="Checking class design (SOLID principles)",
        ),
        # DRY - Check for code duplication
        QualityCheck(
            command=[
                "pylint",
                "src",
                "tests",
                "--disable=all",
                "--enable=duplicate-code",
            ],
            name="DRY checks",
            description="Checking for code duplication (DRY principle)",
        ),
        # Type checking
        QualityCheck(
            command=["mypy", "src", "tests", "--ignore-missing-imports"],
            name="Type checking",
            description="Checking type hints",
        ),
        # Basic formatting
        QualityCheck(
            command=["black", "--check", "src", "tests"],
            name="Code formatting",
            description="Checking code formatting",
        ),
    ]

    all_passed = True
    failed_checks = []
    issues_summary = {}

    for check in checks:
        print(f"\n{check.description}...")
        exit_code, output = run_command(check.command)

        if exit_code != 0:
            print(f"❌ {check.name} failed:")
            print(output)
            all_passed = False
            failed_checks.append(check.name)

            # Extract key issues for summary
            if check.name == "KISS checks" or check.name == "SOLID checks":
                # Extract pylint issues
                import re

                issues = re.findall(
                    r"([A-Za-z0-9_/\\.]+):(\d+):\d+: ([A-Z]\d+): (.+) \((.+)\)", output
                )
                for file, line, code, msg, rule in issues:
                    if file not in issues_summary:
                        issues_summary[file] = []
                    issues_summary[file].append(f"Line {line}: {msg} ({rule})")
            elif check.name == "Type checking":
                # Extract mypy issues
                for line in output.split("\n"):
                    if ": error:" in line:
                        parts = line.split(": error:", 1)
                        file_info = parts[0]
                        error_msg = parts[1].strip()
                        if file_info not in issues_summary:
                            issues_summary[file_info] = []
                        issues_summary[file_info].append(error_msg)
        else:
            print(f"✅ {check.name} passed")

    if all_passed:
        print("\n✅ All quality checks passed!")
    else:
        print("\n❌ Some quality checks failed. Please fix the following issues:\n")

        # Print summary of failed checks
        print("Failed checks:")
        for check in failed_checks:
            print(f"  - {check}")

        # Print summary of issues by file
        if issues_summary:
            print("\nIssues by file:")
            for file, issues in issues_summary.items():
                print(f"\n  {file}:")
                # Limit to top 5 issues per file to keep summary concise
                for i, issue in enumerate(issues[:5]):
                    print(f"    - {issue}")
                if len(issues) > 5:
                    print(f"    ... and {len(issues) - 5} more issues")

        print("\nRun the specific check commands above to see full details.")

    return all_passed


if __name__ == "__main__":
    success = check_code_quality()
    sys.exit(0 if success else 1)
