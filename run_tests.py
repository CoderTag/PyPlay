# run_tests.py
import argparse
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Run automation tests")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="staging")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--browserstack", action="store_true", help="Run on BrowserStack")
    parser.add_argument("--visual", action="store_true", help="Run visual tests")
    parser.add_argument("--parallel", type=int, help="Number of parallel workers")
    parser.add_argument("--tags", help="Tags to filter tests")
    parser.add_argument("--report", choices=["html", "allure"], default="html")
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ["pytest"]
    
    # Add browser option
    cmd.extend(["--browser", args.browser])
    
    # Add environment option
    cmd.extend(["--env", args.env])
    
    # Add headless mode if specified
    if args.headless:
        cmd.append("--headless")
    
    # Add BrowserStack if specified
    if args.browserstack:
        cmd.append("--browserstack")
    
    # Add visual testing if specified
    if args.visual:
        cmd.append("--visual")
    
    # Add parallel execution if specified
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Add tags if specified
    if args.tags:
        cmd.extend(["-m", args.tags])
    
    # Add report option
    if args.report == "allure":
        cmd.extend(["--alluredir", "reports/allure_reports"])
    else:
        cmd.extend(["--html", "reports/html_reports/report.html", "--self-contained-html"])
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    
    # Generate Allure report if selected
    if args.report == "allure":
        subprocess.run(["allure", "generate", "reports/allure_reports", "--clean", "-o", "reports/allure_html"])

if __name__ == "__main__":
    main()