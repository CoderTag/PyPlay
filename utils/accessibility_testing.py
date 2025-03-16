# utils/accessibility_testing.py
import json
from typing import Dict, List, Any

class AccessibilityTester:
    def __init__(self, page):
        self.page = page
    
    async def audit(self) -> Dict[str, Any]:
        """Run accessibility audit using axe-core"""
        # Inject axe-core script
        await self.page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.5.2/axe.min.js")
        
        # Run the audit
        results = await self.page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] }, (err, results) => {
                        resolve(results);
                    });
                });
            }
        """)
        
        return results
    
    def save_results(self, results: Dict[str, Any], filename: str) -> None:
        """Save accessibility results to a file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
    def has_violations(self, results: Dict[str, Any]) -> bool:
        """Check if results contain violations"""
        return len(results.get("violations", [])) > 0