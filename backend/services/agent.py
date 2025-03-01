from browser_use import Agent, Browser, BrowserConfig
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import asyncio
from typing import Dict

class YoutubeService:
    def __init__(self):
        self.browser = Browser(
            config=BrowserConfig(
                chrome_instance_path=os.getenv('CHROME_PATH'),
                headless=False, 
                disable_security=True,
            )
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model='gemini-2.0-flash-exp',
            api_key=os.getenv('GEMINI_API_KEY')
        )
        
        self.context = None  # Will store our browser context

    async def ensure_context(self):
        """Ensure we have a valid browser context"""
        if not self.context:
            self.context = await self.browser.new_context()
        return self.context

    async def process_search_query(self, user_request: str) -> str:
        """Use LLM to extract the most relevant search terms from the user's request."""
        prompt = f"""
        Extract the most relevant search terms for YouTube from this request: "{user_request}"
        Only return the search terms, nothing else. Make it concise but specific.
        Example: "I want to watch funny videos of cats playing piano" -> "funny cats playing piano"
        """
        
        response = await self.llm.apredict(prompt)
        return response.strip()

    async def play_video(self, video_type: str) -> Dict:
        """Search and play a video on YouTube based on the specified type."""
        
        # Process the search query to get relevant terms
        search_query = await self.process_search_query(video_type)
        
        youtube_task = f"""
        Follow these steps precisely:
        1. If there's a YouTube video already playing:
           - Skip step 2 and start from step 3, clicking the search bar at the top of the page
        2. If not already on YouTube:
           - Navigate to https://www.youtube.com
        3. Click the search bar at the top of the page
        4. Search for exactly: {search_query}
        5. From the search results:
           - Look for a video that best matches the requested type
           - Click on the video to play it
        6. Click on the full screen button
        """

        # Get browser context and create agent
        context = await self.ensure_context()
        agent = Agent(
            task=youtube_task,
            llm=self.llm,
            browser_context=context  # Use the persistent context
        )

        try:
            history = await agent.run()
            current_url = None
            
            # Extract URL from history if available
            if hasattr(history, 'urls') and callable(history.urls):
                urls = history.urls()
                if urls:
                    current_url = urls[-1]  # Get the last URL visited
            
            return {
                "status": "success",
                "message": "Video playback initiated",
                "data": {
                    "video_type": video_type,
                    "search_query": search_query,
                    "video_url": current_url or "URL not available",
                    "status": "playing"
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    async def close_browser(self):
        """Close the browser instance."""
        try:
            if self.context:
                await self.context.close()
            await self.browser.close()
        except Exception:
            pass