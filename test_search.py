from tools.search_tool import TavilySearchTool


def main():
    print("Testing TavilySearchTool...")
    tool = TavilySearchTool()

    query = "latest advancements in Generative AI autonomous agents"
    results = tool.search_web(query, max_results=2)

    print(f"\nRetrieved {len(results)} results for query: '{query}'\n")
    for idx, item in enumerate(results, start=1):
        print(f"--- Result {idx} ---")
        print(f"Title  : {item['title']}")
        print(f"URL    : {item['url']}")
        print(f"Snippet: {item['content'][:150]}...")
        print()


if __name__ == "__main__":
    main()