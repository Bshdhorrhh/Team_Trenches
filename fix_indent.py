with open("backend/orchestrator.py", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "router_llm = None" in lines[i]:
        # Get the indentation of the gc.collect() line
        indent = len(lines[i]) - len(lines[i].lstrip())
        
        # Next line is the viz line
        if i + 1 < len(lines):
            viz_line = lines[i+1]
            if "viz =" in viz_line:
                # Re-indent the viz line to match
                lines[i+1] = (" " * indent) + viz_line.lstrip()

with open("backend/orchestrator.py", "w") as f:
    f.writelines(lines)
