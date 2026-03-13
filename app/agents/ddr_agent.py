from langgraph.graph import StateGraph, END
from typing import TypedDict, List

from app.rag.retriever import retrieve_documents
from app.services.conflict_detector import detect_conflicts
from app.services.llm_service import generate_response


class DDRState(TypedDict):
    inspection_text: str
    thermal_text: str
    images: List[str]
    retrieved_context: List[str]
    conflicts: List[str]
    report: str


def retrieve_context(state: DDRState):

    query = state["inspection_text"] + "\n" + state["thermal_text"]

    docs = retrieve_documents(query)

    state["retrieved_context"] = docs

    return state


def detect_document_conflicts(state: DDRState):

    conflicts = detect_conflicts(
        state["inspection_text"],
        state["thermal_text"]
    )

    state["conflicts"] = conflicts

    return state


def generate_report(state: DDRState):

    context_text = "\n".join(state["retrieved_context"])

    images_md = ""

    if state["images"]:
        for img in state["images"]:
            images_md += f"\n![Inspection Image]({img})\n"
    else:
        images_md = "Image Not Available"

    prompt = f"""
Generate a **Detailed Diagnostic Report (DDR)** in clean Markdown.

Inspection Report:
{state["inspection_text"]}

Thermal Report:
{state["thermal_text"]}

Retrieved Context:
{context_text}

Conflicts:
{state["conflicts"]}

Images:
{images_md}

The report MUST follow this structure:

# Detailed Diagnostic Report

## 1. Property Issue Summary

## 2. Area-wise Observations

## 3. Probable Root Cause

## 4. Severity Assessment (with reasoning)

## 5. Recommended Actions

## 6. Additional Notes

## 7. Missing or Unclear Information

Rules:
- Do NOT invent facts
- If information missing write "Not Available"
- Mention conflicts clearly
- Use client-friendly language
"""

    response = generate_response(prompt)

    state["report"] = response

    return state


def build_ddr_agent():

    workflow = StateGraph(DDRState)

    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("detect_conflicts", detect_document_conflicts)
    workflow.add_node("generate_report", generate_report)

    workflow.set_entry_point("retrieve_context")

    workflow.add_edge("retrieve_context", "detect_conflicts")
    workflow.add_edge("detect_conflicts", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()


def run_ddr_agent(inspection_text, thermal_text, images):

    agent = build_ddr_agent()

    initial_state = {
        "inspection_text": inspection_text,
        "thermal_text": thermal_text,
        "images": images,
        "retrieved_context": [],
        "conflicts": [],
        "report": ""
    }

    result = agent.invoke(initial_state)

    return result["report"]