import re

with open("backend/orchestrator.py", "r") as f:
    code = f.read()

pattern = r'coder_llm = self\._get_model\("opencode", required_ctx=oc_ctx\)\s+viz = self\._check_3d_gate\(prompt, ds_answer, router_llm, coder_llm, gen_tokens, gen_temp, status_callback\)'
replacement = r'router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()\n                    viz = self._check_3d_gate(prompt, ds_answer, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)'
code = re.sub(pattern, replacement, code)

pattern2 = r'coder_llm = self\._get_model\("opencode", required_ctx=oc_ctx\)\s+viz = self\._check_3d_gate\(prompt, vibe_answer, router_llm, coder_llm, gen_tokens, gen_temp, status_callback\)'
replacement2 = r'router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()\n                    viz = self._check_3d_gate(prompt, vibe_answer, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)'
code = re.sub(pattern2, replacement2, code)

pattern3 = r'coder_llm = self\._get_model\("opencode", required_ctx=oc_ctx\)\s+viz = self\._check_3d_gate\(prompt, ds_draft, router_llm, coder_llm, gen_tokens, gen_temp, status_callback\)'
replacement3 = r'router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()\n            viz = self._check_3d_gate(prompt, ds_draft, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)'
code = re.sub(pattern3, replacement3, code)

pattern4 = r'coder_llm = self\._get_model\("opencode", required_ctx=oc_ctx\)\s+viz = self\._check_3d_gate\(prompt, vibe_critique, router_llm, coder_llm, gen_tokens, gen_temp, status_callback\)'
replacement4 = r'router_llm = None; ds_llm = None; vibe_llm = None; coder_llm = None; critic_llm = None; model = None; gc.collect()\n            viz = self._check_3d_gate(prompt, vibe_critique, router_ctx, oc_ctx, gen_tokens, gen_temp, status_callback)'
code = re.sub(pattern4, replacement4, code)


with open("backend/orchestrator.py", "w") as f:
    f.write(code)
