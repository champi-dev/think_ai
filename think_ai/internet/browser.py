"""
Headless browser for internet access - Cheap as free!
Using Playwright because it's free and fast.
"""

import asyncio
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Browser, Page
import hashlib
import json
import re
from datetime import datetime, timedelta

from ..utils.logging import get_logger

logger = get_logger(__name__)


class HeadlessBrowser:
    """
    Browse the internet for free using Playwright.
    Like having eyes on the web, but invisible ones! 👻
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context = None
        self.page_cache = {}  # Cache pages for 1 hour
        self.cache_duration = timedelta(hours=1)
        
        # Free search engines (no API needed)
        self.search_engines = {
            'duckduckgo': 'https://duckduckgo.com/?q=',
            'google': 'https://www.google.com/search?q=',
            'bing': 'https://www.bing.com/search?q='
        }
        
        # Blocked domains (to save resources)
        self.blocked_domains = [
            'facebook.com', 'instagram.com', 'tiktok.com',
            'ads.', 'analytics.', 'doubleclick.net'
        ]
        
        logger.info("🌐 Headless browser initialized - Internet access unlocked!")
    
    async def initialize(self):
        """Start the browser engine."""
        try:
            self.playwright = await async_playwright().start()
            
            # Launch with minimal resources
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--disable-gpu',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-images',  # Don't load images (save bandwidth)
                    '--disable-javascript'  # Faster loading for text content
                ]
            )
            
            # Create context with ad blocking
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ThinkAI/1.0'
            )
            
            # Block ads and trackers
            await self.context.route("**/*", self._block_resources)
            
            logger.info("✅ Browser ready - ¡Ey llave, vamo' a surfear! 🏄")
            
        except Exception as e:
            logger.error(f"Browser init failed: {e}")
            logger.info("💡 Install playwright: pip install playwright && playwright install chromium")
    
    async def _block_resources(self, route):
        """Block ads and unnecessary resources to save bandwidth."""
        if any(domain in route.request.url for domain in self.blocked_domains):
            await route.abort()
        elif route.request.resource_type in ['image', 'media', 'font']:
            await route.abort()
        else:
            await route.continue_()
    
    async def search(self, query: str, engine: str = 'duckduckgo') -> Dict[str, Any]:
        """
        Search the web for free!
        Returns top results without costing a penny.
        """
        # Check cache first
        cache_key = hashlib.md5(f"{query}:{engine}".encode()).hexdigest()
        if cache_key in self.page_cache:
            cached = self.page_cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                logger.info("🎯 Cache hit! ¡Qué nota e' vaina!")
                return cached['data']
        
        if not self.browser:
            return {
                'error': 'Browser not initialized',
                'tip': '¡Corre initialize() primero, mi llave!'
            }
        
        try:
            page = await self.context.new_page()
            
            # Navigate to search engine
            search_url = self.search_engines.get(engine, self.search_engines['duckduckgo'])
            await page.goto(search_url + query.replace(' ', '+'))
            
            # Wait for results
            await page.wait_for_selector('body', timeout=5000)
            
            # Extract results based on search engine
            results = await self._extract_search_results(page, engine)
            
            # Cache results
            cache_data = {
                'query': query,
                'engine': engine,
                'results': results,
                'timestamp': datetime.now()
            }
            self.page_cache[cache_key] = {
                'data': cache_data,
                'timestamp': datetime.now()
            }
            
            await page.close()
            
            # Clean old cache entries
            self._clean_cache()
            
            return cache_data
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                'error': str(e),
                'fallback': f'¡Se dañó la búsqueda, pero ey, imagínate la respuesta! 🔮'
            }
    
    async def browse(self, url: str) -> Dict[str, Any]:
        """
        Browse a specific URL and extract content.
        Free web scraping!
        """
        # Check cache
        cache_key = hashlib.md5(url.encode()).hexdigest()
        if cache_key in self.page_cache:
            cached = self.page_cache[cache_key]
            if datetime.now() - cached['timestamp'] < self.cache_duration:
                return cached['data']
        
        if not self.browser:
            return {'error': 'Browser not initialized'}
        
        try:
            page = await self.context.new_page()
            
            # Set timeout and go to page
            await page.goto(url, wait_until='domcontentloaded', timeout=10000)
            
            # Extract content
            content = await self._extract_page_content(page)
            
            # Cache it
            self.page_cache[cache_key] = {
                'data': content,
                'timestamp': datetime.now()
            }
            
            await page.close()
            
            return content
            
        except Exception as e:
            logger.error(f"Browse error: {e}")
            return {
                'error': str(e),
                'url': url,
                'tip': '¿Será que se cayó el sitio? ¡Dale que vamos tarde!'
            }
    
    async def _extract_search_results(self, page: Page, engine: str) -> List[Dict[str, str]]:
        """Extract search results from different engines."""
        results = []
        
        try:
            if engine == 'duckduckgo':
                # DuckDuckGo selectors
                items = await page.query_selector_all('.result__body')
                for item in items[:10]:  # Top 10 results
                    title_elem = await item.query_selector('.result__title')
                    snippet_elem = await item.query_selector('.result__snippet')
                    link_elem = await item.query_selector('.result__url')
                    
                    if title_elem:
                        results.append({
                            'title': await title_elem.inner_text(),
                            'snippet': await snippet_elem.inner_text() if snippet_elem else '',
                            'url': await link_elem.get_attribute('href') if link_elem else ''
                        })
            
            elif engine == 'google':
                # Google selectors
                items = await page.query_selector_all('.g')
                for item in items[:10]:
                    title_elem = await item.query_selector('h3')
                    snippet_elem = await item.query_selector('.VwiC3b')
                    
                    if title_elem:
                        results.append({
                            'title': await title_elem.inner_text(),
                            'snippet': await snippet_elem.inner_text() if snippet_elem else '',
                            'url': 'google.com'  # Google makes URLs tricky
                        })
            
        except Exception as e:
            logger.error(f"Result extraction error: {e}")
        
        return results
    
    async def _extract_page_content(self, page: Page) -> Dict[str, Any]:
        """Extract useful content from a page."""
        try:
            # Get page info
            title = await page.title()
            url = page.url
            
            # Extract text content
            # Remove scripts and styles first
            await page.evaluate('''() => {
                const scripts = document.querySelectorAll('script, style');
                scripts.forEach(el => el.remove());
            }''')
            
            # Get main content
            text_content = await page.evaluate('''() => {
                const body = document.body;
                return body ? body.innerText : '';
            }''')
            
            # Clean up text
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            # Get meta description
            meta_desc = await page.evaluate('''() => {
                const meta = document.querySelector('meta[name="description"]');
                return meta ? meta.content : '';
            }''')
            
            return {
                'title': title,
                'url': url,
                'description': meta_desc,
                'content': text_content[:5000],  # First 5000 chars
                'length': len(text_content),
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content extraction error: {e}")
            return {
                'error': str(e),
                'url': page.url
            }
    
    def _clean_cache(self):
        """Remove old cache entries to save memory."""
        now = datetime.now()
        keys_to_remove = []
        
        for key, cached in self.page_cache.items():
            if now - cached['timestamp'] > self.cache_duration:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.page_cache[key]
        
        if keys_to_remove:
            logger.info(f"🧹 Cleaned {len(keys_to_remove)} old cache entries")
    
    async def shutdown(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        logger.info("👋 Browser closed - ¡Chao pescao!")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get browser statistics."""
        return {
            'cache_size': len(self.page_cache),
            'browser_active': self.browser is not None,
            'search_engines': list(self.search_engines.keys()),
            'blocked_domains': len(self.blocked_domains),
            'status': '¡Bacano parce! ¡Listo pa\' navegar! 🌐'
        }