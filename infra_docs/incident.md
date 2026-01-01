## P1 Incident

### Incident
Incident ID: INC-32587  
Issue: TTC not accessible  

Impacted Services: CareerDomain, EB API, EB ECOM API  
Impacted Portals: Remote-Co, ResumeGenius  

Root Cause: High CPU usage on Neo4j read operations  

Date: 19-Dec-2025

Temporary Fix: Increased CPU requests and HPA max pod count  
Permanent Fix: Implemented query timeout by DEV team

### Incident
Incident ID: INC-32598  
Issue: SOLR cluster node degradation  
 
Impacted Portals: All portals and SOLR-dependent backend services  

Date: 19-Dec-2025  

Cause and Fix (INC-32598): Disk utilization reached 100% on all six SOLR VMs, triggering disk-full alerts and causing two cluster nodes to go down. During disk expansion, affected VMs were restarted but failed to recover and resync data. To resolve this, disk capacity was increased across the SOLR cluster. As stability was not immediately restored, the load balancer was temporarily disabled to reduce backend traffic and allow SOLR collections to recover. Once all collections were synchronized and stable, the load balancer was re-enabled.




