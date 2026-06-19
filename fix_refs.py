import re

with open("backend/orchestrator.py", "r") as f:
    code = f.read()

# Replace:
# coder_llm = self._get_model("opencode", required_ctx=oc_ctx)
# viz = self._check_3d_gate(prompt, compiled_plan, router_llm, coder_llm, gen_tokens, gen_temp, status_callback)
# With:
# router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()
# viz = self._check_3d_gate(prompt, compiled_plan, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)

pattern = r'coder_llm = self\._get_model\("opencode", required_ctx=oc_ctx\)\s+viz = self\._check_3d_gate\(prompt, compiled_plan, router_llm, coder_llm, gen_tokens, gen_temp, status_callback\)'
replacement = r'router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()\n                    viz = self._check_3d_gate(prompt, compiled_plan, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)'

code = re.sub(pattern, replacement, code)

with open("backend/orchestrator.py", "w") as f:
    f.write(code)
