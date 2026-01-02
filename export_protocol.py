#!/usr/bin/env python3
import json
import re

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    protocol = {}
    
    # Context pointers
    current_r_key = None # R0, R1
    current_sub_key = None # R1.1
    
    # Data holders
    current_subsection_data = {}
    
    in_code_block = False
    
    # Regex to extract ID and Title
    # Capture: (Number) (Title)
    # e.g. "0. JERARQUÍA..." -> "0", "JERARQUÍA..."
    
    def extract_header_info(text):
        match = re.match(r"^(\d+(\.\d+)*)\.?\s*(.*)", text)
        if match:
            rid = "R" + match.group(1)
            title = match.group(3).strip()
            return rid, title
        return None, text

    def flush_subsection():
        nonlocal current_subsection_data, current_sub_key, current_r_key
        if current_sub_key and current_r_key:
             # Add content to section
             if current_r_key not in protocol:
                 protocol[current_r_key] = {}
             if "subsections" not in protocol[current_r_key]:
                 protocol[current_r_key]["subsections"] = {}
             
             protocol[current_r_key]["subsections"][current_sub_key] = current_subsection_data
        current_subsection_data = {}
        current_sub_key = None

    def add_content(data_dict, line):
        line = line.strip()
        if not line:
            return
            
        # Detect semantic context from line (if it's a label line)
        # e.g. "**Prohibido:**"
        lower_line = line.lower()
        
        # State tracking for list appending could be complex in a simple loop.
        # We'll use a heuristic: check if the line ITSELF is a rule, or sets a mode.
        # BUT, markdown often has "Prohibido:" then a list.
        # We need to track "current_list_type" in the parent scope or data_dict?
        # data_dict is the dict for the current section/subsection.
        # We can add a "_state" key to it temporarily? Or simpler:
        
        target_list = "rules" # Default
        
        if "**no debe**" in lower_line or "**prohibido**" in lower_line or "ban:" in lower_line:
            data_dict["_current_list"] = "bans"
            # If the line has content beyond the label, add it?
            # Often it's just a header line.
            return 
            
        if "**debe**" in lower_line or "**obligatorio**" in lower_line:
            data_dict["_current_list"] = "obligations"
            return

        if "**permitido**" in lower_line:
             data_dict["_current_list"] = "allowed"
             return
             
        if "**nunca**" in lower_line:
             data_dict["_current_list"] = "absolute_bans"
             return

        # List items
        if line.startswith("- "):
            clean_line = line[2:].strip()
            # Determine list type
            list_type = data_dict.get("_current_list", "rules")
            
            if list_type not in data_dict:
                data_dict[list_type] = []
            data_dict[list_type].append(clean_line)
            
        elif line.startswith("> "):
            clean_line = line[2:].strip().replace("**", "").replace('"', '')
            if "output_templates" not in data_dict:
                data_dict["output_templates"] = []
            data_dict["output_templates"].append(clean_line)
            
        elif line.startswith("```"):
            pass 
            
        else:
             # Numbered lists
             if re.match(r"^\d+\.\s", line):
                 # Treat as steps or ordered rules
                 if "steps" not in data_dict:
                     data_dict["steps"] = []
                 data_dict["steps"].append(line.split(".", 1)[1].strip())
             else:
                 # Loose text
                 # Loose text
                 if "description" not in data_dict:
                     data_dict["description"] = []
                 data_dict["description"].append(line)


    for line in lines:
        line_stripped = line.strip()
        
        if line_stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            # Determine where to add code content
            target = current_subsection_data if current_sub_key else (protocol[current_r_key] if current_r_key else None)
            if target is not None:
                if "code_snippets" not in target:
                    target["code_snippets"] = []
                # Append to last snippet or separate? distinct blocks are better.
                # Simplification: Just dump lines.
                target["code_snippets"].append(line.rstrip())
            continue

        # Headers
        if line.startswith("### "):
            flush_subsection()
            rid, title = extract_header_info(line[4:].strip())
            if rid:
                current_sub_key = rid
                current_subsection_data = {"title": title}
            else:
                 # Fallback for headers without numbers (e.g. "Resultados...")
                 current_sub_key = title # Use title as key if no ID
                 current_subsection_data = {"type": "conceptual_subsection"}

        elif line.startswith("## "):
            flush_subsection()
            rid, title = extract_header_info(line[3:].strip())
            if rid:
                current_r_key = rid
                protocol[current_r_key] = {"title": title}
            else:
                # Non-numbered major sections (e.g. "PRIORIDAD OPERATIVA")
                current_r_key = title
                protocol[current_r_key] = {"type": "conceptual_section"}

        elif line.startswith("# "):
            pass # Ignore global title line for JSON root keys

        else:
            # Content
            target = current_subsection_data if current_sub_key else (protocol[current_r_key] if current_r_key else None)
            if target is not None:
                add_content(target, line)

    # Final flush
    flush_subsection()

    return protocol

if __name__ == "__main__":
    import os
    import shutil
    import datetime
    
    base_path = "/home/saturnxdev/Proyects/Protocol"
    md_path = os.path.join(base_path, "Protocol.md")
    json_path = os.path.join(base_path, "Protocol.json")
    snapshots_dir = os.path.join(base_path, "snapshots")
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found")
        exit(1)
        
    def create_snapshot(target_file):
        if not os.path.exists(target_file):
            return
            
        if not os.path.exists(snapshots_dir):
            os.makedirs(snapshots_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(target_file)
        snapshot_name = f"{filename}_{timestamp}.bak"
        snapshot_path = os.path.join(snapshots_dir, snapshot_name)
        
        shutil.copy2(target_file, snapshot_path)
        print(f"Snapshot created: {snapshot_path}")

    def clean_dict(d):
        if isinstance(d, dict):
            return {k: clean_dict(v) for k, v in d.items() if not k.startswith('_')}
        elif isinstance(d, list):
            return [clean_dict(v) for v in d]
        else:
            return d

    data = parse_markdown(md_path)
    clean_data = clean_dict(data)
    
    create_snapshot(json_path)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported to {json_path}")
