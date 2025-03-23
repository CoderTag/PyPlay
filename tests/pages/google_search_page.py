class GoogleSearchPage:
    def __init__(self, page):
        self.page = page
        self.search_input = 'input[name="q"]'
    
    async def navigate(self):
        await self.page.goto('https://www.google.com')
    
    async def search(self, keyword):
        await self.page.fill(self.search_input, keyword)
        await self.page.press(self.search_input, 'Enter')
    
    async def is_results_displayed(self):
        return await self.page.wait_for_selector('text=pytest-bdd')