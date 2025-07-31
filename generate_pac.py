# File: generate_pac.py
import json
import urllib.request

PROXY_LIST_URL = "http://188.166.142.39/servers/list"

with open("config.json") as f:
    config = json.load(f)

with open("domains.json") as f:
    domains = json.load(f)

# Fetch the proxy list
with urllib.request.urlopen(PROXY_LIST_URL) as response:
    proxy_list = json.loads(response.read().decode())

# Find desired proxy
proxy = next((p for p in proxy_list if p["name"] == config["desired_name"]), None)

if proxy is None:
    raise Exception(f"Proxy named '{config['desired_name']}' not found.")

# Generate PAC script
pac_script = f"""
function FindProxyForURL(url, host) {{
    const domains = {json.dumps(domains)};
    for (let i = 0; i < domains.length; i++) {{
        if (host === domains[i] || host.endsWith('.' + domains[i])) {{
            return "PROXY {proxy['host']}:{proxy['port']}";
        }}
    }}
    return "DIRECT";
}}
"""

with open("proxy.pac", "w") as f:
    f.write(pac_script)

# Write .htaccess with no-cache header
with open(".htaccess", "w") as f:
    f.write('<Files "proxy.pac">\n')
    f.write('  Header set Cache-Control "no-cache, no-store, must-revalidate"\n')
    f.write('</Files>\n')