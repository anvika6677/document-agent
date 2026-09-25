import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Ensure environment variables are loaded
load_dotenv()


class TavilySearchTool:
    """Encapsulates Tavily Search API calls for the agent workflow."""

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY is not set. Please add it to your .env file."
            )
        self.client = TavilyClient(api_key=api_key)

    def search_web(self, query: str, max_results: int = 3) -> list[dict]:
        """Executes a search query and extracts titles, URLs, and clean text snippets.

        Returns:
            list[dict]: A list of clean search results formatted as:
                        [{"title": ..., "url": ..., "content": ...}, ...]
        """
        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
            )

            raw_results = response.get("results", [])
            extracted = []
            for item in raw_results:
                extracted.append(
                    {
                        "title": item.get("title", "No Title"),
                        "url": item.get("url", ""),
                        "content": item.get("content", "").strip(),
                    }
                )
            return extracted

        except Exception as e:
            print(f"[TavilySearchTool Error] Failed to search for '{query}': {e}")
            return []