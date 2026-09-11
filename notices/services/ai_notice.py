import base64
import json

from django.conf import settings
from google import genai


def generate_notice_from_file(uploaded_file, categories):
    """
    Generate title, description and category from
    either a PDF or an image.
    """

    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    category_names = [
        category.category_name
        for category in categories
    ]

    category_text = "\n".join(
        f"- {name}"
        for name in category_names
    )

    # Read uploaded file
    file_bytes = b"".join(uploaded_file.chunks())

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    mime_type = uploaded_file.content_type

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    if mime_type not in allowed_types:
        raise ValueError(
            "Only PDF, JPG, PNG and WEBP files are supported."
        )

    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

    prompt = f"""
You are the official AI assistant for
PUSAT Notice Board, Purbanchal University.

Analyze the uploaded university notice.

The uploaded file may be:
- PDF
- JPG
- PNG
- WEBP

Read the actual content carefully.

Your job is to generate information that an administrator
can use to publish the notice.

AVAILABLE CATEGORIES:

{category_text}

RULES:

1. Generate a short and professional title.

2. Generate a clear and concise description.

3. Choose EXACTLY ONE category from the available categories.

4. NEVER invent a category.

5. NEVER invent information that is not present
   in the uploaded notice.

6. Preserve important:
   - dates
   - deadlines
   - semester information
   - programs
   - departments
   - examination information
   - event information
   - instructions

7. Make the description understandable to
   university students.

8. If the notice contains important information,
   include it in the description.

9. Do not add opinions.

10. Return ONLY valid JSON.

Required JSON:

{{
    "title": "Notice title",
    "description": "Notice description",
    "category": "Existing category"
}}
"""

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=[
            {
                "type": "text",
                "text": prompt,
            },
            {
                "type": "document",
                "data": file_base64,
                "mime_type": mime_type,
            },
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "category": {
                        "type": "string"
                    },
                },
                "required": [
                    "title",
                    "description",
                    "category",
                ],
            },
        },
    )

    result_text = interaction.output_text

    if not result_text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        raise ValueError(
            "AI returned an invalid JSON response."
        )

    return result