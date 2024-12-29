CLEANING_PROMPT_TEMPLATE = """You are tasked with cleaning up and formatting a page of text extracted from an open source project development guide.

Here is the extracted text to work with:

<text>
{markdown_content}
</text>

Follow these steps to clean up and format the text:

1. Carefully review the entire text to understand its content and structure. Understand what is the content of the docs and what is the website elements(irrelevant to the docs).

2. For the website elements(irrelevant to the docs), such as navigation elements, comments, or unrelated content that may have been included due to the extraction process, remove them.

3. Identify and retain only the content of the docs related to the topic of the page.

4. Format the text into proper Markdown, including:
   - Use appropriate heading levels (# for main title, ## for subtitles, etc.)
   - Format code blocks using triple backticks (```) with the appropriate language specified, if applicable
   - Use proper Markdown syntax for lists, bold text, italics, and other formatting elements as needed
   - Preserve any links, converting them to Markdown format: [link text](URL)
   - Maintain the original order and hierarchy of information

Provide your cleaned and formatted Markdown output inside <cleaned_markdown> tags.

Additional guidelines:
- For the Identified docs content,not delete or modify any of them beyond the necessary formatting changes.
- If you encounter any ambiguous sections or are unsure about the relevance of certain content, err on the side of caution and include it in your formatted output.
- Preserve any technical terms, project-specific language, or unique phrasing used in the original text.
- If the original text contains images or diagrams, indicate their presence with a placeholder in your Markdown, e.g., [Image: Description of the image]
- Maintain any numbered lists or step-by-step instructions in their original order.
- Do not translate the text if it is not in English.

Remember, For the identified docs content, do not delete or modify any of them. For the website elements(irrelevant to the docs), removed them """
