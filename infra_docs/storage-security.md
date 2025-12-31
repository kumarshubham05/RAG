## 🔓 Publicly Accessible Storage Accounts (Summary)

The following Azure storage accounts are publicly accessible:

- **devcloudservicearmst**  
  Public network access is enabled. Containers themselves do not allow public access, but the account is reachable from the public internet.


---

## 🎯 Purpose

- Identify storage accounts that are **publicly reachable**
- Identify containers with **public blob access**
- Track **owners** and **approved exceptions**
- Support **security reviews, audits, and compliance**

---

## 🚨 Key Definitions

- **Network Access = Allow**  
  → Storage account is reachable over the public internet

- **Container Access = Blob**  
  → Blobs inside the container are publicly readable

- **Container Access = Off**  
  → No public access

---

## 🔓 Storage Accounts with Public Network Access

### devcloudservicearmst

- **Subscription:** COMMONSERVICES-DEV-TEST-AZURE
- **Resource Group:** DEV-CLOUDSERVICE-RG
- **Network Access:** **Allow (Public)**
- **Approved Exception:** INF-37063_99991231
- **Owners:**
  - Ankur Garg
  - Piyush Jain

#### Containers
| Container Name | Public Access |
|---------------|---------------|
| dev-api-rex | Off |
| hp-sandbox-api-rex | Off |
| perf-api-rex | Off |
| sandbox-api-rex | Off |
| sandbox-importtool-cloud-arm | Off |

> ⚠️ Although the storage account is publicly reachable, **no containers are publicly accessible**.

---

## 🌐 Containers with Public Blob Access Enabled

### adpocstg20122024

- **Subscription:** COMMONSERVICES-DEV-TEST-AZURE
- **Resource Group:** adpocrg20122024
- **Network Access:** Deny
- **Owners:**
  - Ankur Garg
  - Piyush Jain

| Container | Access |
|---------|--------|
| diagnostics-dumps | **Blob (Public)** |

---

### bolddev

- **Subscription:** COMMONSERVICES-DEV-TEST-AZURE
- **Resource Group:** DEVOPS-RG
- **Network Access:** Deny
- **Owner:** Baroon Anand

| Container | Access |
|---------|--------|
| argoswebjob | **Blob (Public)** |
| documentstorage | **Blob (Public)** |
| documentstorage-backup | **Blob (Public)** |
| legacymagentadocuments | **Blob (Public)** |
| sampledocuments-dev | **Blob (Public)** |

---

## 🔒 Storage Accounts with No Public Network Access

### companies

- **Subscription:** COMMONSERVICES-DEV-TEST-AZURE
- **Resource Group:** DEV-APP-RG
- **Network Access:** Deny
- **Owners:**
  - Hemant Kumar
  - Rajender Sharma

| Container | Access |
|---------|--------|
| backupsqldev | Blob |
| logo | Blob |

> ℹ️ Containers allow blob access, but **public network access is denied**, reducing exposure.

---

## 🛡️ Security Notes

- Public network access and container access **must be evaluated together**
- Public blob access should be **explicitly approved**
- Approved exceptions must be **periodically reviewed**
- No secrets should ever be stored in publicly accessible containers

---

## 📅 Governance

- **Maintained By:** DevOps / Cloud Security Team
- **Last Reviewed:** _(add date)_
- **Next Review:** Quarterly or on infrastructure changes

---

## 🔍 Example Questions This Assistant Can Answer

- Which Azure storage accounts are publicly accessible?
- Are any storage containers publicly open?
- Who owns the `bolddev` storage account?
- Which containers have public blob access?
- Does `devcloudservicearmst` have public access?

---
