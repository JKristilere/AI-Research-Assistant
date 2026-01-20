import requests
from typing import List, Dict
from crewai.tools import BaseTool
import json


class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "Searches the web for information on a given topic. "
        "Returns a list of relevant URLs and snippets. "
        "Input should be a search query string."
    )

    def _run(self, query:str):
        """
        Execute web search using DuckDuckGo API (no key required)
        """

        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html":1,
                "skip_disambig":1
            }

            response = requests.get(url=url, params=params, timeout=10)
            data = response.json()

            results = []

            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Summary"),
                    "snippet": data.get("Abstract"),
                    "url": data.get("AbstractURL", ""),
                    "source": data.get("AbstractSource", "DuckDuckGo")
                })
            

            for topic in data.get("RelatedTopics", [])[:5]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                        "source": "DuckDuckGo"
                    })
            
            if not results:
                return json.dumps({
                    "status": "no_results",
                    "message": f"No results found for query: {query}",
                    "results": []
                })
            
            return json.dumps({
                "status": "success",
                "query": query,
                "results": results[:10]
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Search failed: {str(e)}",
                "results": []
            })