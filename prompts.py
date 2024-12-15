CLEANING_PROMPT_TEMPLATE = """You are tasked with cleaning up and formatting a page of text extracted from an open source project development guide. Your goal is to present the information in a clean, well-organized Markdown format while maintaining the original meaning and important information. It's crucial that you do not add, remove, or modify any content beyond the necessary formatting changes.

Here is the extracted text to work with:

<text>
{markdown_content}
</text>

Follow these steps to clean up and format the text:

1. Carefully review the entire text to understand its content and structure.

2. Remove any irrelevant parts, such as navigation elements, comments, or unrelated content that may have been included due to the extraction process.

3. Identify and retain only the main content related to the topic of the page.

4. Format the text into proper Markdown, including:
   - Use appropriate heading levels (# for main title, ## for subtitles, etc.)
   - Format code blocks using triple backticks (```) with the appropriate language specified, if applicable
   - Use proper Markdown syntax for lists, bold text, italics, and other formatting elements as needed
   - Preserve any links, converting them to Markdown format: [link text](URL)
   - Maintain the original order and hierarchy of information

Provide your cleaned and formatted Markdown output inside <cleaned_markdown> tags.

Additional guidelines:
- Do not delete or modify any of the original content beyond the necessary formatting changes.
- If you encounter any ambiguous sections or are unsure about the relevance of certain content, err on the side of caution and include it in your formatted output.
- Preserve any technical terms, project-specific language, or unique phrasing used in the original text.
- If the original text contains images or diagrams, indicate their presence with a placeholder in your Markdown, e.g., [Image: Description of the image]
- Maintain any numbered lists or step-by-step instructions in their original order.
- Do not translate the text if it is not in English.

Remember, your primary goal is to improve the formatting and readability of the text while preserving all original content and meaning. Do not add any new information or remove any existing information from the original text."""
