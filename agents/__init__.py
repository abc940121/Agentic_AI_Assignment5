import os
import importlib
from llm_loader import load_local_llm

class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register_agents(self):
        # Dynamically discover and register agents from subdirectories
        base_path = os.path.dirname(__file__)
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                try:
                    # Look for agent.py in each subfolder
                    module_name = f"agents.{item}.agent"
                    module = importlib.import_module(module_name)
                    
                    # Look for classes ending with 'Agent'
                    for attr_name in dir(module):
                        if attr_name.endswith("Agent") and not attr_name.startswith("Base"):
                            cls = getattr(module, attr_name)
                            self.agents[item] = cls()
                            print(f"[Registry] Registered agent: {item} ({attr_name})")
                except Exception as e:
                    print(f"[Registry] Failed to load agent from {item}: {e}")

_registry = AgentRegistry()

def build_ncu_pipeline():
    load_local_llm()
    if not _registry.agents:
        _registry.register_agents()
    
    # Map internal names to registry keys
    # Note: the directory names are used as keys
    return {
        "nlu": _registry.agents.get("nlu"),
        "security": _registry.agents.get("security"),
        "planner": _registry.agents.get("planner"),
        "executor": _registry.agents.get("executor"),
        "diagnosis": _registry.agents.get("diagnosis"),
        "repair": _registry.agents.get("repair"),
        "explanation": _registry.agents.get("explanation"),
    }
