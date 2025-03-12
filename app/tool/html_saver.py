import os

import aiofiles

from app.tool.base import BaseTool, ToolResult
from app.tool.browser_use_tool import BrowserUseTool


class HtmlSaver(BaseTool):
    name: str = "html_saver"
    description: str = """Open a browser and nevigate to the specified url.
Save the html content of the specified url to a local file at a specified path.
Use this tool when you need to save html content of the specified url to a file on the local filesystem.
The tool accepts a url and a file path, and saves the html content of the url to that location.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "(required) The url that browser opened.",
            },
            "file_path": {
                "type": "string",
                "description": "(required) The path where the file should be saved, including filename and extension.",
            },
            "mode": {
                "type": "string",
                "description": "(optional) The file opening mode. Default is 'w' for write. Use 'a' for append.",
                "enum": ["w", "a"],
                "default": "w",
            },
        },
        "required": ["url", "file_path"],
    }

    async def execute(self, url: str, file_path: str, mode: str = "w") -> str:
        """
        Save the html content of the specified url to a file at the specified path.

        Args:
            url (str): The url that browser opened.
            file_path (str): The path where the file should be saved.
            mode (str, optional): The file opening mode. Default is 'w' for write. Use 'a' for append.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            browser = BrowserUseTool()
            await browser.execute(action="navigate", url=url);
            result:ToolResult = await browser.execute(action="get_html");

            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write directly to the file
            async with aiofiles.open(file_path, mode, encoding="utf-8") as file:
                await file.write(result.output)

            return f"Content successfully saved to {file_path}"
        except Exception as e:
            return f"Error saving file: {str(e)}"
