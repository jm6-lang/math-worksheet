import subprocess
import json

# 搜索 WordPress 资源站主题
searches = [
    "WordPress theme VIP member download",
    "ripro WordPress",
    "zibll theme",
    "WordPress 资源站 主题",
]

for query in searches:
    print(f"\n=== 搜索: {query} ===")
    result = subprocess.run(
        ['gh', 'api', f'search/repositories?q={query.replace(" ", "+")}&sort=stars&per_page=5'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        for item in data.get('items', []):
            print(f"  - {item['full_name']} ({item['stargazers_count']} stars)")
            print(f"    {item.get('description', 'N/A')[:60] if item.get('description') else 'N/A'}")
            print(f"    {item['html_url']}")
    else:
        print(f"  搜索失败: {result.stderr}")