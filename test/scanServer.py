import httpx

def scan_server(url):
    server = "Not disclosed"
    x_powered_by = "Not found"
    cdn_str = "None detected"
    waf_str = "None detected"
    protocols = set()
    
    try:
        with httpx.Client(http2=True, timeout=10) as client:
            r = client.get(url)
            protocols.add(r.http_version)
            
            server = r.headers.get("Server", server)
            x_powered_by = r.headers.get("X-Powered-By", x_powered_by)
            
            alt_svc = r.headers.get("Alt-Svc", "")
            if "h3" in alt_svc:
                protocols.add("HTTP/3")
            
            cdn = []
            if r.headers.get("CF-RAY"):
                cdn.append("Cloudflare")
            if r.headers.get("X-Amz-Cf-Id"):
                cdn.append("AWS CloudFront")
            if r.headers.get("X-Akamai-Request-ID"):
                cdn.append("Akamai")
            if server and "cloudflare" in server.lower():
                cdn.append("Cloudflare")
            if server and "akamai" in server.lower():
                cdn.append("Akamai")
            
            if cdn:
                cdn_str = ", ".join(set(cdn))
            
            waf = []
            if r.headers.get("CF-RAY"):
                waf.append("Cloudflare WAF")
            if r.headers.get("X-Sucuri-ID"):
                waf.append("Sucuri WAF")
            if r.headers.get("X-Mod-Security"):
                waf.append("ModSecurity")
            if r.headers.get("X-AWS-WAF"):
                waf.append("AWS WAF")
            if r.headers.get("X-Akamai-Request-ID"):
                waf.append("Akamai WAF")
            
            if waf:
                waf_str = ", ".join(set(waf))
                
    except Exception:
        pass
    
    if "HTTP/1.1" not in protocols:
        try:
            with httpx.Client(http2=False, timeout=10) as client:
                r = client.get(url)
                protocols.add(r.http_version)
        except Exception:
            pass
    
    protocol_str = ", ".join(sorted(protocols)) if protocols else "Unknown"
    
    print(f"Server: {server}")
    print(f"Server Version: {x_powered_by}")
    print(f"CDN Service: {cdn_str}")
    print(f"WAF Service: {waf_str}")
    print(f"HTTP Protocol Support: {protocol_str}")