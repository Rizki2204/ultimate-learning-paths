# scripts/encyclopedia/fix_quotes.py
import os
import re

DIR = os.path.dirname(__file__)
files = [
    'missing_tier_6.py', 'missing_tier_7.py', 'missing_tier_8.py',
    'missing_tier_9.py', 'missing_tier_10.py', 'missing_tier_11.py'
]

for fname in files:
    path = os.path.join(DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: "code_block": """..."""
    # Replace any """ inside the code_block with \"\"\"
    parts = content.split('"code_block": """')
    new_parts = [parts[0]]
    for p in parts[1:]:
        subparts = p.split('""",\n        "pitfalls":')
        if len(subparts) == 2:
            cb_body = subparts[0]
            rest = subparts[1]
            # Replace triple quotes inside cb_body
            cb_body_escaped = cb_body.replace('\\"\\"\\"', '___ESCAPED_TQ___')
            cb_body_escaped = cb_body_escaped.replace('"""', '\\"\\"\\"')
            cb_body_escaped = cb_body_escaped.replace('___ESCAPED_TQ___', '\\"\\"\\"')
            new_parts.append(cb_body_escaped + '""",\n        "pitfalls":' + rest)
        else:
            new_parts.append(p)

    fixed = '"code_block": """'.join(new_parts)
    # Also fix invalid escape sequences like \S and \$ in regular strings
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print(f"Processed {fname}")

# Now test compilation
all_ok = True
for fname in files:
    path = os.path.join(DIR, fname)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, path, 'exec')
        print(f"Compile {fname}: OK")
    except SyntaxError as e:
        print(f"Compile {fname}: SyntaxError at line {e.lineno}: {e.msg}")
        all_ok = False

if all_ok:
    print("ALL 6 MISSING TIER FILES COMPILE CLEANLY!")
