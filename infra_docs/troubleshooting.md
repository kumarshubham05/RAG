## Apache SOLR Troubleshooting

To troubleshoot Apache SOLR issues please follow this [Confluence Doc](https://livecareer.atlassian.net/wiki/spaces/INFRA/pages/4255449263/Apache+Solr+Troubleshooting)

## 403 Forbidden Error Troubleshooting

Meaning: Request is blocked by the destination service  
Cause: Source IP not allowed  
Action 1: Identify outbound IPs of the calling service  
Action 2: Identify the destination service  
Fix 1: Whitelist source IP on destination service  
Azure Case: If both services run on Azure with Service Endpoints enabled  
Azure Fix: Whitelist source subnet on destination service
 
## 502 Bad Gateway (Azure, AKS, WordPress, Cloudflare, Akamai)

Meaning: Gateway received an invalid response from upstream service  

### Cloudflare/Akamai
Cause: Origin server unreachable  
Cause: Origin returned invalid HTTP response  
Cause: Origin timeout  
Cause: SSL/TLS mode mismatch (Flexible / Full / Strict)  
Cause: Cloudflare/Akamai IPs blocked by firewall  

### Azure Web App
Cause: Backend endpoint unreachable  
Cause: App timeout exceeded  
Cause: Backend returned invalid response  
Cause: TLS/SSL mismatch  

### AKS
Cause: Pod not running or crashing  
Cause: Service has no healthy endpoints  
Cause: Ingress cannot reach service  
Cause: Readiness or liveness probe failure  
Cause: Pod response timeout  

### WordPress on Linux VM
Cause: Web server not running (NGINX/Apache)  
Cause: PHP-FPM not responding  
Cause: High CPU or memory usage  
Cause: Disk full  
Cause: NSG or firewall blocking traffic  

### Network / Integration
Cause: Incorrect backend URL or port  
Cause: DNS resolution failure  
Cause: Firewall or NSG blocking traffic  

