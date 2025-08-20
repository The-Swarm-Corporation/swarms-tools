import importlib
import subprocess
import sys


def lazy_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Installing missing package: {module_name}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", module_name],
            check=True,
        )
        return importlib.import_module(module_name)


# Lazy load required packages
asyncio = lazy_import("asyncio")
aiohttp = lazy_import("aiohttp")
BeautifulSoup = lazy_import("bs4").BeautifulSoup
json = lazy_import("json")
os = lazy_import("os")
List, Dict, Optional = (
    lazy_import("typing").List,
    lazy_import("typing").Dict,
    lazy_import("typing").Optional,
)
load_dotenv = lazy_import("dotenv").load_dotenv
Console = lazy_import("rich.console").Console
(
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
) = (
    lazy_import("rich.progress").Progress,
    lazy_import("rich.progress").SpinnerColumn,
    lazy_import("rich.progress").TextColumn,
    lazy_import("rich.progress").BarColumn,
    lazy_import("rich.progress").TimeRemainingColumn,
)
Panel = lazy_import("rich.panel").Panel
html2text = lazy_import("html2text")
ThreadPoolExecutor, as_completed = (
    lazy_import("concurrent.futures").ThreadPoolExecutor,
    lazy_import("concurrent.futures").as_completed,
)
sync_playwright = lazy_import("playwright.sync_api").sync_playwright
time = lazy_import("time")
retry, stop_after_attempt, wait_exponential = (
    lazy_import("tenacity").retry,
    lazy_import("tenacity").stop_after_attempt,
    lazy_import("tenacity").wait_exponential,
)
datetime = lazy_import("datetime").datetime
re = lazy_import("re")

console = Console()
load_dotenv()


class WebSearch:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.outputs_dir = "search_results"
        os.makedirs(self.outputs_dir, exist_ok=True)

        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = True
        self.html_converter.ignore_images = True
        self.html_converter.ignore_emphasis = True

        self.max_retries = 2
        self.max_threads = 5  # Reduced concurrency for stability
        self.timeout = 15

    async def fetch_search_results(self, query: str) -> List[Dict]:
        """Fetch search results from Google Custom Search API"""
        async with aiohttp.ClientSession() as session:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_cx,
                "q": query,
                "num": 10,
            }

            try:
                async with session.get(
                    url, params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            {
                                "title": item.get(
                                    "title", "No title"
                                ),
                                "url": item["link"],
                                "snippet": item.get("snippet", ""),
                                "source": "Google Search",
                            }
                            for item in data.get("items", [])
                            if "link" in item
                            and not any(
                                ext in item["link"].lower()
                                for ext in [".pdf", ".doc", ".docx"]
                            )
                        ][:10]
                    return []
            except Exception as e:
                console.print(f"[red]Search error: {str(e)}[/red]")
                return []

    def _preprocess_html(self, raw_html: str) -> str:
        """
        Raw HTML preprocessor that handles common issues before parsing
        - Removes unnecessary elements
        - Normalizes structure
        - Extracts potential content sections
        """
        # Remove script and style elements completely
        cleaned_html = re.sub(
            r"<(script|style).*?>.*?</\1>",
            "",
            raw_html,
            flags=re.DOTALL,
        )

        # Remove common tracking pixels
        cleaned_html = re.sub(
            r'<img[^>]+src=".*?(track|pixel|beacon).*?"[^>]*>',
            "",
            cleaned_html,
            flags=re.IGNORECASE,
        )

        # Normalize div structure
        cleaned_html = re.sub(r"<div[^>]*>", "<div>", cleaned_html)

        # Extract potential content containers
        content_match = re.search(
            r"<body.*?>(.*?)</body>",
            cleaned_html,
            re.DOTALL | re.IGNORECASE,
        )

        return (
            content_match.group(1) if content_match else cleaned_html
        )

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Improved content extraction using hybrid parsing
        Combines CSS selection with semantic analysis
        """
        # First try standard semantic tags
        selectors = [
            "article",
            "main",
            "div.article",
            "div.content",
            "div.main-content",
            "div.post-content",
            "section.content",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element and len(element.text) > 500:
                return str(element)

        # Fallback to body content analysis
        body = soup.find("body")
        if body:
            # Find the most text-dense section
            paragraphs = body.find_all(["p", "div"])
            max_length = 0
            best_candidate = None

            for p in paragraphs:
                text_length = len(p.text)
                if text_length > max_length:
                    max_length = text_length
                    best_candidate = p

            return str(best_candidate) if best_candidate else ""

        return ""

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=5),
    )
    def extract_content(self, url: str) -> Optional[Dict]:
        """Enhanced extraction with raw HTML preprocessing"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True, timeout=15000
                )
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    java_script_enabled=True,  # Keep JS enabled for modern sites
                )

                page = context.new_page()
                page.set_default_timeout(10000)

                try:
                    # Get raw HTML after basic rendering
                    page.goto(url, wait_until="domcontentloaded")
                    raw_html = page.content()

                    # Preprocess raw HTML
                    processed_html = self._preprocess_html(raw_html)

                    # Create soup from processed HTML
                    soup = BeautifulSoup(processed_html, "lxml")

                    # Remove residual unwanted elements
                    for element in soup(
                        [
                            "nav",
                            "footer",
                            "header",
                            "aside",
                            "form",
                            "iframe",
                        ]
                    ):
                        element.decompose()

                    # Extract main content
                    main_content = self._extract_main_content(soup)

                    # Convert to clean text
                    clean_text = (
                        self.html_converter.handle(main_content)
                        if main_content
                        else ""
                    )
                    clean_text = " ".join(
                        clean_text.split()
                    )  # Normalize whitespace

                    return {
                        "url": url,
                        "title": (
                            soup.title.string.strip()
                            if soup.title
                            else "No title"
                        ),
                        "content": (
                            clean_text[:3000] + "..."
                            if len(clean_text) > 3000
                            else clean_text
                        ),
                    }

                finally:
                    browser.close()

        except Exception as e:
            console.print(
                f"[yellow]Content extraction warning: {url} - {str(e)}[/yellow]"
            )
            return None

    async def process_urls(self, urls: List[str]) -> List[Dict]:
        """Process URLs with improved error handling"""
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                "Processing websites...", total=len(urls)
            )

            with ThreadPoolExecutor(
                max_workers=self.max_threads
            ) as executor:
                future_to_url = {
                    executor.submit(self.extract_content, url): url
                    for url in urls
                }

                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        if result := future.result():
                            results.append(result)
                    except Exception as e:
                        console.print(
                            f"[red]Processing error: {url} - {str(e)}[/red]"
                        )
                    finally:
                        progress.advance(task)

        return results

    def format_results(self, query: str, results: List[Dict]) -> str:
        """Improved formatting with fallback content"""
        formatted = [
            f"## Web Search Results: {query}",
            "\n---\n",
            f"Found {len(results)} results\n",
        ]

        for i, result in enumerate(results, 1):
            content_preview = (
                result.get("content")
                or result.get("snippet")
                or "Content unavailable"
            )
            formatted.extend(
                [
                    f"{i}. {result['title']}",
                    f"   URL: {result['url']}",
                    f"   Preview: {content_preview[:500].split('\n')[0]}...",
                    "\n---\n",
                ]
            )

        return "\n".join(formatted)

    async def search(self, query: str) -> str:
        """Main search workflow with enhanced reliability"""
        start_time = time.time()

        # Get search results
        search_data = await self.fetch_search_results(query)
        if not search_data:
            return "No search results found."

        # Process URLs
        urls = [result["url"] for result in search_data]
        extracted_data = await self.process_urls(urls)

        # Create URL map for efficient lookup
        content_map = {
            item["url"]: item for item in extracted_data if item
        }

        # Merge results with fallback
        merged_results = []
        for original in search_data:
            merged_results.append(
                {
                    **original,
                    "content": (
                        content_map.get(original["url"], {}).get(
                            "content", ""
                        )
                    ),
                }
            )

        # Format results
        formatted_results = self.format_results(query, merged_results)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(
            self.outputs_dir, f"search_{timestamp}.txt"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted_results)

        console.print(
            Panel(
                f"✅ Search completed in {time.time() - start_time:.1f}s\n"
                f"📄 Results saved to: [underline]{filename}[/underline]",
                title="Search Complete",
                border_style="green",
            )
        )

        return formatted_results


def test_content_extraction(html_file: str):
    with open(html_file, "r", encoding="utf-8") as f:
        raw_html = f.read()

    searcher = WebSearch()
    processed_html = searcher._preprocess_html(raw_html)
    soup = BeautifulSoup(processed_html, "lxml")
    main_content = searcher._extract_main_content(soup)

    console.print("\n[bold]Extracted Content:[/bold]\n")
    console.print(main_content[:2000] + "...")


def web_search(query: str) -> str:
    """Synchronous entry point"""
    searcher = WebSearch()
    return asyncio.run(searcher.search(query))


# if __name__ == "__main__":
#     results = web_search("AI latest news")
#     console.print("\n[bold]Formatted Results:[/bold]\n")
#     console.print(results)
