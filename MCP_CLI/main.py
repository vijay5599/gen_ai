from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from urllib.parse import urlencode
import asyncio

base_url = "https://server.smithery.ai/@smithery/toolbox/mcp"
params = {
    "api_key": "7292be34-3982-4bdc-b80f-6aacb74c9005",
    "profile": "willowy-giraffe-mb2SQ0"
}
url = f"{base_url}?{urlencode(params)}"

async def main():
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 1: Search for servers about "math"
            print("\n🔎 Searching for math servers...")
            servers = await session.call_tool("search_servers", {"query": "math"})
            print("Search results:", servers)

            if not servers.results:
                print("⚠️ No math servers found, try another query.")
                return

            # Step 2: Pick the first server
            server_url = servers.results[0]["url"]
            print(f"\n✅ Using server: {server_url}")

            # Step 3: List tools on this server
            tool_list = await session.call_tool("use_tool", {
                "server_url": server_url,
                "tool": "__list_tools__",
                "input": {}
            })
            print("\n📦 Tools on server:", tool_list)

            # Step 4: Call the 'add' tool if available
            if "add" in str(tool_list):
                result = await session.call_tool("use_tool", {
                    "server_url": server_url,
                    "tool": "add",
                    "input": {"a": 5, "b": 7}
                })
                print("\n➕ Add Result:", result)
            else:
                print("\n⚠️ No 'add' tool found on this server")

if __name__ == "__main__":
    asyncio.run(main())
