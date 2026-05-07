"""
Dependency Health Check
Pings external URLs to ensure dependencies are healthy before deployment.
"""
import urllib.request
import urllib.error
import time
import socket

def run_dependency_check(check_cfg):
    """
    Check external dependency health by pinging configured URLs.
    """
    urls = check_cfg.get("urls", [])
    warn_latency = float(check_cfg.get("warn_latency", 3.0))

    if not urls:
        return {"status": "SKIP", "message": "No dependency URLs configured in .graveyard.yml"}

    results = []
    has_error = False
    has_warning = False

    for dep in urls:
        if isinstance(dep, dict):
            name = dep.get("name", dep.get("url", "unknown"))
            url = dep.get("url")
            timeout = float(dep.get("timeout", 5.0))
        else:
            name = str(dep)
            url = str(dep)
            timeout = 5.0

        if not url:
            continue
            
        if not url.startswith("http"):
            url = "https://" + url

        try:
            start_time = time.time()
            
            # Create request with a User-Agent to avoid getting blocked by some APIs
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Graveyard-CLI/1.0'}
            )
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                latency = time.time() - start_time
                status_code = response.getcode()
                
                # Check HTTP status (200-399 is considered OK for a basic health ping)
                if status_code >= 400:
                    results.append(f"{name} ❌ (HTTP {status_code})")
                    has_error = True
                elif latency > warn_latency:
                    results.append(f"{name} ⚠ slow ({latency:.2f}s > {warn_latency}s)")
                    has_warning = True
                else:
                    results.append(f"{name} ✓ ({latency:.2f}s)")
                    
        except urllib.error.URLError as e:
            # e.g., ConnectionRefused, DNS failure
            results.append(f"{name} ❌ ({getattr(e, 'reason', str(e))})")
            has_error = True
        except socket.timeout:
            results.append(f"{name} ❌ (Timeout > {timeout}s)")
            has_error = True
        except Exception:
            results.append(f"{name} ❌ (Error)")
            has_error = True

    if has_error:
        return {"status": "FAIL", "message": ", ".join(results)}
    elif has_warning:
        return {"status": "WARN", "message": ", ".join(results)}
    
    return {"status": "PASS", "message": ", ".join(results)}
