"""
Script to verify code quality.

This script analyzes the codebase for SOLID, KISS, and DRY compliance.
"""
import sys
import os
import subprocess
import re
from typing import Dict, Any, List, Tuple, Set

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_pylint() -> Tuple[bool, str]:
    """
    Run pylint on the codebase.
    
    Returns:
        Tuple of (success, output)
    """
    print("Running pylint...")
    result = subprocess.run(
        ["pylint", "src", "--disable=C0111,C0103,C0303,W0511,R0903,R0913,R0914,R0801"],
        capture_output=True,
        text=True
    )
    
    return result.returncode == 0, result.stdout


def analyze_solid_compliance(files: List[str]) -> Dict[str, Any]:
    """
    Analyze SOLID compliance.
    
    Args:
        files: List of files to analyze
        
    Returns:
        Dictionary with analysis results
    """
    print("Analyzing SOLID compliance...")
    
    # Initialize results
    results = {
        "single_responsibility": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        },
        "open_closed": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        },
        "liskov_substitution": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        },
        "interface_segregation": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        },
        "dependency_inversion": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        }
    }
    
    # Patterns to check
    srp_pattern = re.compile(r"class\s+\w+.*?:.*?def\s+\w+.*?def\s+\w+.*?def\s+\w+.*?def\s+\w+.*?def\s+\w+.*?def\s+\w+", re.DOTALL)
    ocp_pattern = re.compile(r"if\s+isinstance\(.*?\).*?elif\s+isinstance\(.*?\)", re.DOTALL)
    lsp_pattern = re.compile(r"if\s+type\(.*?\)\s+==\s+.*?:", re.DOTALL)
    isp_pattern = re.compile(r"class\s+\w+\(.*?\).*?pass", re.DOTALL)
    dip_pattern = re.compile(r"from\s+src\.core\s+import", re.MULTILINE)
    
    for file_path in files:
        if not file_path.endswith(".py"):
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check Single Responsibility Principle
            if srp_pattern.search(content):
                results["single_responsibility"]["non_compliant"] += 1
                results["single_responsibility"]["non_compliant_files"].append(file_path)
            else:
                results["single_responsibility"]["compliant"] += 1
            
            # Check Open/Closed Principle
            if ocp_pattern.search(content):
                results["open_closed"]["non_compliant"] += 1
                results["open_closed"]["non_compliant_files"].append(file_path)
            else:
                results["open_closed"]["compliant"] += 1
            
            # Check Liskov Substitution Principle
            if lsp_pattern.search(content):
                results["liskov_substitution"]["non_compliant"] += 1
                results["liskov_substitution"]["non_compliant_files"].append(file_path)
            else:
                results["liskov_substitution"]["compliant"] += 1
            
            # Check Interface Segregation Principle
            if isp_pattern.search(content) and "interface" in file_path:
                results["interface_segregation"]["non_compliant"] += 1
                results["interface_segregation"]["non_compliant_files"].append(file_path)
            else:
                results["interface_segregation"]["compliant"] += 1
            
            # Check Dependency Inversion Principle
            if dip_pattern.search(content) and "domain" in file_path:
                results["dependency_inversion"]["non_compliant"] += 1
                results["dependency_inversion"]["non_compliant_files"].append(file_path)
            else:
                results["dependency_inversion"]["compliant"] += 1
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")
    
    return results


def analyze_kiss_compliance(files: List[str]) -> Dict[str, Any]:
    """
    Analyze KISS compliance.
    
    Args:
        files: List of files to analyze
        
    Returns:
        Dictionary with analysis results
    """
    print("Analyzing KISS compliance...")
    
    # Initialize results
    results = {
        "function_length": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        },
        "cyclomatic_complexity": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        }
    }
    
    # Patterns to check
    function_pattern = re.compile(r"def\s+\w+\(.*?\).*?(?=def|\Z)", re.DOTALL)
    complexity_pattern = re.compile(r"if.*?(?:and|or).*?(?:and|or).*?:", re.DOTALL)
    
    for file_path in files:
        if not file_path.endswith(".py"):
            continue
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check function length
            functions = function_pattern.findall(content)
            long_functions = [f for f in functions if f.count("\n") > 20]
            
            if long_functions:
                results["function_length"]["non_compliant"] += 1
                results["function_length"]["non_compliant_files"].append(file_path)
            else:
                results["function_length"]["compliant"] += 1
            
            # Check cyclomatic complexity
            if complexity_pattern.search(content):
                results["cyclomatic_complexity"]["non_compliant"] += 1
                results["cyclomatic_complexity"]["non_compliant_files"].append(file_path)
            else:
                results["cyclomatic_complexity"]["compliant"] += 1
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")
    
    return results


def analyze_dry_compliance(files: List[str]) -> Dict[str, Any]:
    """
    Analyze DRY compliance.
    
    Args:
        files: List of files to analyze
        
    Returns:
        Dictionary with analysis results
    """
    print("Analyzing DRY compliance...")
    
    # Initialize results
    results = {
        "code_duplication": {
            "compliant": 0,
            "non_compliant": 0,
            "non_compliant_files": []
        }
    }
    
    # Run duplicate code detection
    try:
        result = subprocess.run(
            ["pylint", "src", "--disable=all", "--enable=duplicate-code"],
            capture_output=True,
            text=True
        )
        
        # Check for duplicate code
        if "Similar lines" in result.stdout:
            duplicate_files = set()
            for line in result.stdout.split("\n"):
                if line.startswith("src/"):
                    duplicate_files.add(line.split(":")[0])
            
            results["code_duplication"]["non_compliant"] = len(duplicate_files)
            results["code_duplication"]["non_compliant_files"] = list(duplicate_files)
            results["code_duplication"]["compliant"] = len(files) - len(duplicate_files)
        else:
            results["code_duplication"]["compliant"] = len(files)
    except Exception as e:
        print(f"Error running duplicate code detection: {str(e)}")
    
    return results


def calculate_compliance_score(results: Dict[str, Any]) -> float:
    """
    Calculate overall compliance score.
    
    Args:
        results: Analysis results
        
    Returns:
        Compliance score (0-100)
    """
    total_compliant = 0
    total_files = 0
    
    # SOLID compliance
    for principle in ["single_responsibility", "open_closed", "liskov_substitution", "interface_segregation", "dependency_inversion"]:
        total_compliant += results["solid"][principle]["compliant"]
        total_files += results["solid"][principle]["compliant"] + results["solid"][principle]["non_compliant"]
    
    # KISS compliance
    for metric in ["function_length", "cyclomatic_complexity"]:
        total_compliant += results["kiss"][metric]["compliant"]
        total_files += results["kiss"][metric]["compliant"] + results["kiss"][metric]["non_compliant"]
    
    # DRY compliance
    total_compliant += results["dry"]["code_duplication"]["compliant"]
    total_files += results["dry"]["code_duplication"]["compliant"] + results["dry"]["code_duplication"]["non_compliant"]
    
    if total_files == 0:
        return 0
    
    return (total_compliant / total_files) * 100


def get_python_files() -> List[str]:
    """
    Get all Python files in the project.
    
    Returns:
        List of Python file paths
    """
    python_files = []
    
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    return python_files


def verify_code_quality() -> bool:
    """
    Verify code quality.
    
    Returns:
        True if verification passes, False otherwise
    """
    print("Verifying code quality...")
    
    # Get all Python files
    files = get_python_files()
    print(f"Found {len(files)} Python files.")
    
    # Run pylint
    pylint_success, pylint_output = run_pylint()
    if not pylint_success:
        print("Pylint found issues:")
        print(pylint_output)
    
    # Analyze SOLID compliance
    solid_results = analyze_solid_compliance(files)
    
    # Analyze KISS compliance
    kiss_results = analyze_kiss_compliance(files)
    
    # Analyze DRY compliance
    dry_results = analyze_dry_compliance(files)
    
    # Combine results
    results = {
        "solid": solid_results,
        "kiss": kiss_results,
        "dry": dry_results
    }
    
    # Calculate compliance score
    compliance_score = calculate_compliance_score(results)
    print(f"Overall compliance score: {compliance_score:.2f}%")
    
    # Check if compliance is adequate
    if compliance_score < 93:
        print("Compliance score is below 93%, which is not adequate.")
        return False
    
    print("Verification passed: Code quality is adequate.")
    return True


if __name__ == "__main__":
    success = verify_code_quality()
    sys.exit(0 if success else 1)
