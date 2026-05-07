"""
JUnit XML Test Results Parser
"""
import os
import xml.etree.ElementTree as ET

def parse_junit_xml(file_path):
    """
    Parse a single JUnit XML file and return totals.
    Handles standard JUnit structure (<testsuites> and <testsuite>).
    """
    results = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Determine if root is <testsuites> or <testsuite>
        if root.tag == "testsuites":
            # Some runners put totals on the root element
            if "tests" in root.attrib:
                results["tests"] = int(root.attrib.get("tests", 0))
                results["failures"] = int(root.attrib.get("failures", 0))
                results["errors"] = int(root.attrib.get("errors", 0))
                results["skipped"] = int(root.attrib.get("skipped", 0))
                return results
                
            # Otherwise aggregate from <testsuite> children
            for suite in root.findall("testsuite"):
                results["tests"] += int(suite.attrib.get("tests", 0))
                results["failures"] += int(suite.attrib.get("failures", 0))
                results["errors"] += int(suite.attrib.get("errors", 0))
                results["skipped"] += int(suite.attrib.get("skipped", 0))
                
        elif root.tag == "testsuite":
            results["tests"] = int(root.attrib.get("tests", 0))
            results["failures"] = int(root.attrib.get("failures", 0))
            results["errors"] = int(root.attrib.get("errors", 0))
            results["skipped"] = int(root.attrib.get("skipped", 0))
            
    except Exception as e:
        print(f"\033[93mWarning: Failed to parse JUnit file {file_path}: {e}\033[0m")
        
    return results

def get_test_results(tests_path):
    """
    Parse all XML files in a directory or a single file.
    """
    total_results = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    
    if not os.path.exists(tests_path):
        return None, f"Path not found: {tests_path}"
        
    files_to_parse = []
    
    if os.path.isfile(tests_path):
        if tests_path.endswith('.xml'):
            files_to_parse.append(tests_path)
    else:
        for root, _, files in os.walk(tests_path):
            for file in files:
                if file.endswith('.xml'):
                    files_to_parse.append(os.path.join(root, file))
                    
    if not files_to_parse:
        return None, "No .xml files found in tests path"
        
    for f in files_to_parse:
        res = parse_junit_xml(f)
        total_results["tests"] += res["tests"]
        total_results["failures"] += res["failures"]
        total_results["errors"] += res["errors"]
        total_results["skipped"] += res["skipped"]
        
    return total_results, None

def run_test_check(tests_path, check_cfg):
    """
    Check test results against configured thresholds.
    """
    if not tests_path:
        return {"status": "SKIP", "message": "No test results path provided (use --tests)"}

    min_pass = check_cfg.get("min_pass_rate", 95)
    
    # Coverage is not standardized in JUnit XML, usually requires Cobertura/Jacoco parser
    # For now, we will focus purely on test pass rate
    
    results, err = get_test_results(tests_path)
    if err:
        return {"status": "WARN", "message": err}
        
    total = results["tests"]
    
    if total == 0:
        return {"status": "FAIL", "message": "No tests found in provided XML files"}
        
    failed = results["failures"] + results["errors"]
    passed = total - failed - results["skipped"]
    
    # Calculate pass rate based on executed tests (ignoring skipped)
    executed = total - results["skipped"]
    if executed == 0:
        return {"status": "WARN", "message": f"All {total} tests were skipped"}
        
    pass_rate = round((passed / executed) * 100, 1)
    
    if pass_rate < min_pass:
        return {
            "status": "FAIL",
            "message": f"{passed}/{executed} passed ({pass_rate}%) — below {min_pass}% threshold"
        }

    return {
        "status": "PASS",
        "message": f"{passed}/{executed} passed ({pass_rate}% — threshold: {min_pass}%)"
    }
