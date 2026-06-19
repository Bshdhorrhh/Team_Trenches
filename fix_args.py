with open("backend/orchestrator.py", "r") as f:
    code = f.read()

# Fix _coding_pipeline signature
code = code.replace(
    "def _coding_pipeline(self, prompt, enriched_prompt, router_llm,\n                         ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback=None):",
    "def _coding_pipeline(self, prompt, enriched_prompt, router_llm,\n                         router_ctx, ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback=None):"
)

# Fix _reasoning_pipeline signature
code = code.replace(
    "def _reasoning_pipeline(self, prompt, enriched_prompt, router_llm,\n                            ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback=None):",
    "def _reasoning_pipeline(self, prompt, enriched_prompt, router_llm,\n                            router_ctx, ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback=None):"
)

# Fix calls in process_query
code = code.replace(
    "return self._coding_pipeline(prompt, enriched_prompt, router_llm,\n                                         ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)",
    "return self._coding_pipeline(prompt, enriched_prompt, router_llm,\n                                         router_ctx, ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)"
)

code = code.replace(
    "return self._reasoning_pipeline(prompt, enriched_prompt, router_llm,\n                                        ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)",
    "return self._reasoning_pipeline(prompt, enriched_prompt, router_llm,\n                                        router_ctx, ds_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)"
)

with open("backend/orchestrator.py", "w") as f:
    f.write(code)
