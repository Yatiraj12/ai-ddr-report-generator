from app.services.llm_service import generate_response


def generate_ddr_report(
    inspection_text: str,
    thermal_text: str,
    retrieved_context: list,
    conflicts: list,
    images: list
):
    """
    Generate structured DDR report
    """

    context_text = "\n".join(retrieved_context)

    images_section = ""

    if images:
        for img in images:
            images_section += f"\n![Inspection Image]({img})"
    else:
        images_section = "Image Not Available"

    prompt = f"""
Generate a Detailed Diagnostic Report (DDR).

Inspection Observations:
{inspection_text}

Thermal Observations:
{thermal_text}

Additional Context:
{context_text}

Conflicts Identified:
{conflicts}

Images extracted from reports:
{images_section}

The report MUST follow this structure:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

Rules:
- Do NOT invent facts
- If information missing write "Not Available"
- Clearly mention conflicts
- Use simple client friendly language
"""

    report = generate_response(prompt)

    return report