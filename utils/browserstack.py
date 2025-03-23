# utils/browserstack_utils.py
import os
import json
import requests

def update_browserstack_status(session_id, passed):
    """Update BrowserStack test status"""
    username = os.environ.get("BROWSERSTACK_USERNAME")
    access_key = os.environ.get("BROWSERSTACK_ACCESS_KEY")
    
    url = f"https://api.browserstack.com/automate/sessions/{session_id}.json"
    
    status = "passed" if passed else "failed"
    
    payload = {
        "status": status,
        "reason": ""
    }
    
    response = requests.put(
        url,
        auth=(username, access_key),
        data=json.dumps(payload)
    )
    
    return response.status_code == 200

def get_session_id(page):
    """Extract BrowserStack session ID"""
    if hasattr(page, "browser_context") and hasattr(page.browser_context, "browser"):
        browser = page.browser_context.browser
        if hasattr(browser, "_channel"):
            # This is a hack and may need to be adjusted based on how Playwright
            # exposes the BrowserStack session information
            session_info = browser._channel.send("Browser.getInfo")
            return session_info.get("sessionId")
    return None