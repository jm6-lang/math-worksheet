import json

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\dup_report.json', encoding='utf-8') as f:
    r = json.load(f)

for d in ['movies', 'curriculum']:
    print(f'\n=== {d} ===')
    info = r[d]
    for title, files in info['dups'].items():
        print(f'  Title: {title}')
        for fn in files:
            fi = info['file_info'][fn]
            has_body = fi.get('has_body', False)
            quark = fi.get('quark_link', '')
            heading = fi.get('heading_title', '')
            body = fi.get('body_preview', '')
            print(f'    {fn}: body={has_body}')
            print(f'    heading: {heading}')
            print(f'    quark: {quark}')
            print(f'    body: {body}')
