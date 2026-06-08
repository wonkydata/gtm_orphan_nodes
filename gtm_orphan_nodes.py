# Wonkydata.com LLC
#
# gtm_orphan_nodes.py
#

import json
import pandas as pd


def find_hermit_nodes(gtm_json_path):
    # Load the GTM export file
    with open(gtm_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    container_version = data.get("containerVersion", {})

    # Extract the main components
    tags = container_version.get("tag", [])
    triggers = container_version.get("trigger", [])
    variables = container_version.get("variable", [])

    # Build dictionaries for easy lookup
    tag_map = {t["tagId"]: t["name"] for t in tags}
    trigger_map = {tr["triggerId"]: tr["name"] for tr in triggers}
    variable_map = {v["variableId"]: v["name"] for v in variables}

    # Track what is being used (referenced)
    used_triggers = set()
    used_variables = set()

    # --- Step 1: Analyze Tags ---
    for tag in tags:
        # Check triggers causing the tag to fire
        for trigger_id in tag.get("firingTriggerId", []):
            used_triggers.add(trigger_id)
        # Check exception triggers
        for trigger_id in tag.get("blockingTriggerId", []):
            used_triggers.add(trigger_id)

        # Check for variables used inside tag parameters
        for param in tag.get("parameter", []):
            val = str(param.get("value", ""))
            # GTM variables are referenced as {{Variable Name}}
            for var_id, var_name in variable_map.items():
                if f"{{{{{var_name}}}}}" in val: # Corrected f-string
                    used_variables.add(var_id)

    # --- Step 2: Analyze Triggers ---
    for trigger in triggers:
        # Check for variables used in trigger filters (conditions)
        for filter_cond in trigger.get("filter", []):
            for param in filter_cond.get("parameter", []):
                val = str(param.get("value", ""))
                for var_id, var_name in variable_map.items():
                    if f"{{{{{var_name}}}}}" in val: # Corrected f-string
                        used_variables.add(var_id)

    # --- Step 3: Analyze Variables ---
    # Variables can reference other variables
    for variable in variables:
        for param in variable.get("parameter", []):
            val = str(param.get("value", ""))
            for var_id, var_name in variable_map.items():
                # Prevent a variable from marking itself as 'used' if it mentions its own name
                if variable["variableId"] != var_id and f"{{{{{var_name}}}}}" in val: # Corrected f-string
                    used_variables.add(var_id)

    # --- Step 4: Identify the Hermits ---
    # 1. Hermit Triggers (Not used by any tag)
    hermit_triggers = [
        name for tid, name in trigger_map.items() if tid not in used_triggers
    ]

    # 2. Hermit Variables (Not used by any tag, trigger, or other variable)
    # Exclude GTM built-in system variables if they are in the list
    hermit_variables = [
        name for vid, name in variable_map.items() if vid not in used_variables
    ]

    # 3. Hermit Tags (Tags are 'hermits' if they have no firing triggers)
    hermit_tags = [
        tag["name"]
        for tag in tags
        if not tag.get("firingTriggerId") and not tag.get("blockingTriggerId")
    ]

    # --- Step 5: Display Results ---
    print(f"## COLD, LONELY HERMIT NODES FOUND ##\n# Input JSON File: {gtm_json_path}\n")

    print(f"Total Tags Evaluated: {len(tags)} (Hermit: {len(hermit_tags)})")
    print(f"Total Triggers Evaluated: {len(triggers)} (Hermit: {len(hermit_triggers)})")
    print(f"Total Variables Evaluated: {len(variables)} (Hermit: {len(hermit_variables)})\n")
    print("-" * 40)

    print(f"\n[!] Hermit Tags ({len(hermit_tags)}) - No firing triggers:")
    for t in hermit_tags:
        print(f"  - {t}")

    print(f"\n[!] Hermit Triggers ({len(hermit_triggers)}) - Not attached to any tag:")
    for tr in hermit_triggers:
        print(f"  - {tr}")

    print(f"\n[!] Hermit Variables ({len(hermit_variables)}) - Never referenced:")
    for v in hermit_variables:
        print(f"  - {v}")


# Run the script (Replace "GTM-your-file.json" with your actual JSON export file path)
if __name__ == "__main__":
    # Example: find_hermit_nodes('GTM-your-file.json')
    find_hermit_nodes("GTM-your-file.json")
