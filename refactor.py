import re

with open("backend/orchestrator.py", "r") as f:
    content = f.read()

# Replace _call_model signature
content = content.replace(
    "def _call_model(self, llm, prompt, max_tokens=512, temperature=0.7):",
    "def _call_model(self, model_key, required_ctx, prompt, max_tokens=512, temperature=0.7):\n        llm = self._get_model(model_key, required_ctx=required_ctx)"
)

# Now fix all calls.
# From: self._call_model(router_llm, p, max_tokens=10, temperature=0.1)
# To: self._call_model("router", router_ctx, p, max_tokens=10, temperature=0.1)

# We need to map the variables to their keys and ctx variables.
# router_llm -> "router", router_ctx
# model -> "router", router_ctx (in _is_playground_applicable, let's check its signature)
# critic_llm -> "vibethinker", ds_ctx
# coder_llm -> "opencode", oc_ctx
# ds_llm -> "deepseek_r1", ds_ctx
# vibe_llm -> "vibethinker", ds_ctx

mapping = {
    "router_llm": ('"router"', "router_ctx"),
    "ds_llm": ('"deepseek_r1"', "ds_ctx"),
    "vibe_llm": ('"vibethinker"', "ds_ctx"),
    "coder_llm": ('"opencode"', "oc_ctx"),
    "critic_llm": ('"vibethinker"', "ds_ctx"),
    "model": ('"deepseek_r1"', "ds_ctx") # wait, _run_playground uses ds_llm or vibe_llm. It's passed as 'model'.
}

# We need to manually fix the method signatures that take llms as arguments.
