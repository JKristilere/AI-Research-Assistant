import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool 
import json
import validators
from config.settings import settings

class WebScraperTool(BaseTool):
    name: str = "Web Scraper Tool"
    description: str = (
        "Scrapes content from a given URL and extracts main text, headings, and metadata. "
        "Input should be a valid URL string."
    )
    
    def _run(self, url: str) -> str:
        """
        Scrape and extract content from a webpage
        """
        try:
            # Validate URL
            if not validators.url(url):
                return json.dumps({
                    "status": "error",
                    "message": "Invalid URL provided",
                    "content": None
                })
            
            # Fetch page content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=settings.SCRAPING_TIMEOUT
            )
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "aside"]):
                script.decompose()
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.string if title else "No title"
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc and meta_desc.get('content') else ""
            
            # Extract headings
            headings = []
            for heading in soup.find_all(['h1', 'h2', 'h3'])[:10]:
                headings.append({
                    "level": heading.name,
                    "text": heading.get_text(strip=True)
                })
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                # Get paragraphs
                paragraphs = [p.get_text(strip=True) for p in main_content.find_all('p')]
                content_text = '\n\n'.join([p for p in paragraphs if len(p) > 50])[:5000]
            else:
                content_text = soup.get_text(separator='\n', strip=True)[:5000]
            
            result = {
                "status": "success",
                "url": url,
                "title": title_text,
                "description": description,
                "headings": headings,
                "content": content_text,
                "word_count": len(content_text.split())
            }
            
            return json.dumps(result, indent=2)
            
        except requests.exceptions.Timeout:
            return json.dumps({
                "status": "error",
                "message": "Request timed out",
                "content": None
            })
        except requests.exceptions.RequestException as e:
            return json.dumps({
                "status": "error",
                "message": f"Failed to fetch URL: {str(e)}",
                "content": None
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Scraping failed: {str(e)}",
                "content": None
            })