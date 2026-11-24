import json
from pathlib import Path
from datetime import datetime, timezone


MEMORY_FILE = Path(__file__).resolve().parents[2] / "memory" / "agent_memory.json"


def load_memories(path=MEMORY_FILE):
    """Load previously saved workflow memories."""

    path = Path(path)

    if not path.exists() or path.stat().st_size == 0:
        return []

    with path.open("r", encoding="utf-8-sig") as file:
        memories = json.load(file)

    if not isinstance(memories, list):
        raise ValueError("Memory file must contain a JSON list")

    return memories

def save_memory(state, path=MEMORY_FILE):
    """Save a completed workflow to persistent memory."""

    if state["status"] != "completed":
        raise ValueError("Only completed workflows can be saved")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    memories = load_memories(path)

    memory = {
        "user_request": state["user_request"],
        "research_findings": state["research_findings"],
        "analysis": state["analysis"],
        "final_response": state["final_response"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    memories.append(memory)

    temp_path = path.with_name(path.name + ".tmp")

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(memories, file, indent=4, ensure_ascii=False)

    temp_path.replace(path)

    return memory


def get_recent_memories(limit=5, path=MEMORY_FILE):
    """Return the most recent workflow memories."""

    if limit < 1:
        raise ValueError("Limit must be greater than zero")

    memories = load_memories(path)

    return memories[-limit:]
def retrieve_relevant_memories(user_request, limit=3, path=MEMORY_FILE):
    """Retrieve previous workflows using keyword matching."""

    memories = load_memories(path)

    stop_words = {
        "the", "and", "for", "with", "what",
        "how", "was", "were", "are", "is",
        "about", "from", "that", "this"
    }

    request_words = {
        word.lower().strip(".,?!")
        for word in user_request.split()
        if len(word) > 2 and word.lower() not in stop_words
    }

    scored_memories = []

    for memory in memories:
        searchable_text = " ".join([
            memory.get("user_request", ""),
            str(memory.get("research_findings", "")),
            str(memory.get("analysis", ""))
        ]).lower()

        memory_words = {
            word.strip(".,?!")
            for word in searchable_text.split()
            if len(word) > 2
        }

        score = len(request_words.intersection(memory_words))

        if score > 0:
            scored_memories.append((score, memory))

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        memory
        for score, memory in scored_memories[:limit]
    ]