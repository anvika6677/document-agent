from typing import TypedDict, List, Dict, Optional, Any


class AgentState(TypedDict):
    request: str
    planned_sections: List[Dict[str, Any]]
    research_context: str
    sources: List[Dict[str, str]]
    generated_content: Dict[str, str]
    final_sections: List[Dict[str, str]]
    output_file: Optional[str]
    error: Optional[str]