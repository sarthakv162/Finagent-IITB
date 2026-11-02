"""DOM distillation utility to produce LLM-friendly page state summaries."""

from __future__ import annotations

from typing import Dict, List, Optional

from bs4 import BeautifulSoup


def _normalized_text(node) -> str:
    text = node.get_text(" ", strip=True)
    return " ".join(text.split())


def _build_label_map(soup: BeautifulSoup) -> Dict[str, str]:
    label_map: Dict[str, str] = {}
    for label in soup.find_all("label"):
        target_id = label.get("for")
        if target_id:
            label_map[target_id] = _normalized_text(label)
    # Also handle labels that wrap inputs directly
    for label in soup.find_all("label"):
        input_child = label.find("input")
        if input_child and input_child.get("id"):
            label_map[input_child["id"]] = _normalized_text(label)
    return label_map


def distill_dom(html: str) -> Dict[str, List[Dict[str, Optional[str]]]]:
    """Convert raw HTML into a simplified semantic snapshot.

    Removes scripts/styles/meta and extracts buttons, inputs, links, and
    error/success messages. Output is selector-free for LLM consumption.
    """

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "meta"]):
        tag.decompose()

    label_map = _build_label_map(soup)

    buttons: List[Dict[str, Optional[str]]] = []
    actionable_controls = soup.find_all("button") + soup.find_all(
        "input", {"type": ["button", "submit", "reset"]}
    )
    for btn in actionable_controls:
        buttons.append(
            {
                "role": btn.get("role", "button"),
                "text": _normalized_text(btn),
            }
        )

    inputs: List[Dict[str, Optional[str]]] = []
    for inp in soup.find_all("input"):
        if inp.get("type", "text").lower() in {"hidden"}:
            continue
        input_id = inp.get("id")
        inputs.append(
            {
                "type": inp.get("type", "text"),
                "placeholder": inp.get("placeholder"),
                "label": label_map.get(input_id),
            }
        )

    links: List[Dict[str, Optional[str]]] = []
    for anchor in soup.find_all("a"):
        links.append(
            {
                "text": _normalized_text(anchor),
                "href": anchor.get("href"),
            }
        )

    messages: List[Dict[str, Optional[str]]] = []
    message_tags = soup.find_all(
        lambda tag: tag.has_attr("class")
        and any(cls for cls in tag.get("class", []) if "error" in cls.lower() or "success" in cls.lower())
        or tag.get("role") == "alert"
    )
    for msg in message_tags:
        cls = " ".join(msg.get("class", [])) if msg.has_attr("class") else None
        messages.append(
            {
                "kind": "success" if cls and "success" in cls.lower() else "error" if cls and "error" in cls.lower() else None,
                "text": _normalized_text(msg),
            }
        )

    return {
        "buttons": buttons,
        "inputs": inputs,
        "links": links,
        "messages": messages,
    }


__all__ = ["distill_dom"]