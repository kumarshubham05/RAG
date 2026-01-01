## Core Site Architecture

Entry Point: Akamai  
Security Layer: Akamai WAF evaluates rules  
Delivery Layer: Akamai CDN evaluates rules  
Cache Hit: Content served from Akamai CDN  
Cache Miss: Request forwarded to Portal Web App  
Backend: Portal Web App calls microservices which are hosted on other webapps and AKS. 
CMS: WordPress CMS is a dependent microservice

## Core Site Names

Livecareer
Resume-Now
Myperfectresume
Coverletter-Now
Flexjobs
Remote-Co

## Off Site Architecture
Entry Point: Cloudflare  
Security Layer: Cloudflare WAF evaluates rules  
Delivery Layer: Cloudflare CDN evaluates rules  
Cache Hit: Content served from Cloudflare CDN  
Cache Miss: Request forwarded to Portal Web App  
Backend: Portal Web App calls microservices which are hosted on other webapps and AKS. 
CMS: WordPress CMS is a dependent microservice

## Off Brand Site Names

ResuemGenius
Resume Help
CVGENIUS
Resumecompanion
ResumeNERD

## WordPress SSG Architecture

Rendering Model: Static Site Generation (SSG)  
Backend VMs: Used for content scraping and generation  
Backend Stack: WordPress with PHP-FPM  
Database: Azure PaaS SQL Database  
Frontend VMs: Serve static content  
Frontend Stack: NGINX serves static files

