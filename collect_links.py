import json

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\dup_report.json', encoding='utf-8') as f:
    r = json.load(f)

for d in ['movies', 'curriculum']:
    info = r[d]
    for title, files in info['dups'].items():
        for fn in files:
            fi = info['file_info'][fn]
            quark = fi.get('quark_link', '')
            if quark:
                print(d, fn, quark)
