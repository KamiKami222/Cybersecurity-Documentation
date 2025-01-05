# Postman API Project

This project demonstrates building and testing an API using Flask, with Postman (Desktop Agent) as the testing tool. 
The API supports network diagnostic tools like:
- ping
- DNS lookup
- Traceroute

Notes regarding API Keys used in this project:
- The user must first generate an API-Key and include it in the x-api-key header of the request to access the API endpoints.
- API keys will be hashed (SHA256) and then stored server side to enhance key security.
- To better demonstrate expiration of keys, the server will save only the last key generated as "active" and will de-activated all previous generated keys. I've gone with this route of key expiration because this is a single user API demo and it enables more "comfy" testing instead of having a static expiration timer.

---

## Table of Contents
1. [Overview](#1-overview)
2. [Setup Instructions](#2-setup-instructions)
3. [API Endpoints](#3-api-endpoints)
4. [Testing with Postman](#4-testing-with-postman)
5. [Challenges and Learnings](#5-challenges-and-learnings)

---

## 1. Overview

### Objective
- Build a network diagnostic API with endpoints for:
  - **Ping:** Test connectivity to a target.
  - **DNS Lookup:** Resolve a domain to its IP address.
  - **Traceroute:** Trace the route to a target.
  - **Generate API Key:** Secure API endpoints.

### Tools Used
- **Flask**: Framework for building the API.
- **Postman**: Testing and debugging API requests. (Desktop Agent to access locally hosted API)

---

## 2. Setup Instructions

### Prerequisites
- Python 3.7 or newer.
- Flask installed (see dependencies below).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo/projects/api

---

## 3. API Endpoints

API will be hosted at http://127.0.0.1:5000/ENDPOINTs

General Errors:
- **405 Method Not Allowed:** The Method is not allowed for the requsted URL.
- **404 Not Found:** The Requested URL was not found on the server. 
- **401 Unauthorized:** If the API key is missing or invalid.
- **400 Bad Request:** If the domain field is missing in the request body.
- **500 Internal Server Error:** If the domain cannot be resolved.

### Key Generation - `/api/key`

- **Method:** `POST`
- **Description:** Generates a new API key for authenticating subsequent requests.
- **Headers:** None required.
- **Request Body:** None required.
- **Response:**
  ```json
  {
      "api_key": "your_generated_api_key_here",
      "message": "New API key generated."
      
  }
  
### DNS Lookup - `/api/dns`

- **Method:** `POST`
- **Description:** Performs DNS lookup for the provided target.
- **Headers:** x-api-key - Your API Key here.
- **Request Body:** 
  ```json
  {
    "domain": "www.target.com"
  }

- **Response:**
  ```json
  {
  "domain": "www.target.com",
  "ip": "x.x.x.x"
  }

### Traceroute - `/api/traceroute`

- **Method:** `POST`
- **Description:** Performs tracert to test hops to the target.
- **Headers:** x-api-key - Your API Key here.
- **Request Body:** 
  ```json
  {
    "target": "www.google.com"
  }

- **Response:**
  ```json
  {
  "result": "\nTracing route to www.google.com [142.250.75.68]\nover a maximum of 30 hops:\n\n  1     3 ms     3 ms     3 ms  netbox [10.100.102.1] \n  2     7 ms     7 ms     7 ms  10.255.250.4 \n  3     6 ms     6 ms     9 ms  core1-cbng5-4014.rhn.nv.net.il [207.232.10.156] \n  4     8 ms     9 ms     8 ms  core1-nta-core1-rhn-BE2291.nv.net.il [212.143.12.229] \n  5     6 ms     7 ms     6 ms  peering2-27-core1-nta.nta.nv.net.il [212.143.203.29] \n  6    11 ms     8 ms     9 ms  192.178.69.74 \n  7     8 ms     9 ms     9 ms  108.170.229.65 \n  8     8 ms     7 ms     8 ms  142.251.228.197 \n  9     8 ms     7 ms     7 ms  tztlva-ab-in-f4.1e100.net [142.250.75.68] \n\nTrace complete.\n",
  "target": "www.google.com"
  }

### Ping - `/api/ping`

- **Method:** `POST`
- **Description:** Tests connectivity by pinging the target.
- **Headers:** x-api-key - Your API Key here.
- **Request Body:** 
  ```json
  {
    "target": "www.target.com"
  }

- **Response:**
  ```json
  {
  "result": "\nPinging www.google.com [142.250.75.164] with 32 bytes of data:\nReply from 142.250.75.164: bytes=32 time=7ms TTL=117\n\nPing statistics for 142.250.75.164:\n    Packets: Sent = 1, Received = 1, Lost = 0 (0% loss),\nApproximate round trip times in milli-seconds:\n    Minimum = 7ms, Maximum = 7ms, Average = 7ms\n",
  "target": "www.google.com"
  }

### Key Logs - `/api/logs` - **This endpoint is intentionally vulnerable and will reveal the logged keys without authenticating the user, I'm planning to try Pass-The-Hash attack on an API in the future**.

- **Method:** `GET`
- **Description:** Provides detailed logs of previously created keys.
- **Headers:** None required.
- **Request Body:** None required
- **Response:**
  ```json
  [
  {
    "api_key_hashed": "8e255e822c183f318ecea54eda57158ab01d86b10fecdf7c8a61fdf59bda7c34",
    "created_at": "2025-01-04 18:06:38.243613",
    "id": 1,
    "status": "inactive"
  },
  .
  .
  .
  .
  
  {
    "api_key_hashed": "b43af87776d020bedc3d3d58b0ab14a9662083cc0ca4dcbd3275e9be903b3bc4",
    "created_at": "2025-01-06 00:40:29.403366",
    "id": 18,
    "status": "active"
  }
  ]
  




