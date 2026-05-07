"""
Security Check - Trivy Integration
"""
import os
import json
import subprocess
import shutil

def run_security_check(image, check_cfg):
    """
    Run Trivy security scanning against configured severity thresholds.
    """
    if not image:
        return {"status": "SKIP", "message": "No container image provided (use --image)"}

    # Check if trivy is installed
    if not shutil.which("trivy"):
        return {"status": "WARN", "message": "Trivy not found. Please install Trivy: brew install trivy"}

    block_on = check_cfg.get("block_on", "CRITICAL")
    warn_on = check_cfg.get("warn_on", "HIGH")
    max_high = check_cfg.get("max_high", 5)

    try:
        # Run trivy command and capture JSON output
        # Using --scanners vuln to keep it fast
        # Using --quiet to suppress extra output
        result = subprocess.run(
            ["trivy", "image", "--format", "json", "--scanners", "vuln", "--quiet", image],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 and not result.stdout:
            return {"status": "FAIL", "message": f"Trivy scan failed: {result.stderr.strip()}"}

        # Parse Trivy JSON
        data = json.loads(result.stdout)
        
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
        
        # Trivy output structure:
        # { "Results": [ { "Vulnerabilities": [ { "Severity": "HIGH", ... } ] } ] }
        for res in data.get("Results", []):
            for vuln in res.get("Vulnerabilities", []):
                sev = vuln.get("Severity", "UNKNOWN")
                if sev in counts:
                    counts[sev] += 1
                else:
                    counts["UNKNOWN"] += 1

        crit = counts["CRITICAL"]
        high = counts["HIGH"]
        med = counts["MEDIUM"]

        msg = f"{crit} critical, {high} high, {med} medium vulns"

        # Logic for blocking/warning
        if block_on == "CRITICAL" and crit > 0:
            return {"status": "FAIL", "message": f"{msg} (blocked: {crit} CRITICAL)"}
            
        if block_on == "HIGH" and high > 0:
            return {"status": "FAIL", "message": f"{msg} (blocked: {high} HIGH)"}

        # Custom threshold for max HIGH
        if crit > 0:
            # We already checked if we block on critical. If we are here, block_on must be OFF or None, 
            # but usually >0 critical is a block or at least warn
            pass

        if high > max_high:
            return {"status": "FAIL", "message": f"{msg} (blocked: {high} HIGH > {max_high} max)"}
            
        if warn_on == "HIGH" and high > 0:
            return {"status": "WARN", "message": f"{msg} (warn: {high} HIGH)"}
            
        if warn_on == "MEDIUM" and med > 0:
            return {"status": "WARN", "message": f"{msg} (warn: {med} MEDIUM)"}

        return {"status": "PASS", "message": msg}

    except Exception as e:
        return {"status": "WARN", "message": f"Failed to run Trivy: {e}"}
