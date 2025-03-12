import asyncio

from app.tool.html_saver import HtmlSaver


async def main():
    htmlSaver = HtmlSaver()
    await htmlSaver.execute(url="https://www.baidu.com", file_path="baidu.html")

if __name__ == "__main__":
    asyncio.run(main())