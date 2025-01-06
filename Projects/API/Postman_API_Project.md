# Postman API Project

This project demonstrates building and testing an API using Flask, with Postman (Desktop Agent) as the testing tool. 
The API supports network diagnostic tools like:
- ping
- DNS lookup
- Traceroute

Notes regarding API Keys used in this project:
- The user must first generate an API-Key and include it in the x-api-key header of the request to access the API endpoints.
- API keys will be hashed (SHA256) and then stored server side to enhance key security.
- To better demonstrate key expiration, the server saves only the last key generated as "active" and deactivates all previously generated keys. I've gone with this route of key expiration because this is a single user API demo and it enables more "comfy" testing instead of having a static expiration timer.

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

API will be hosted at http://127.0.0.1:5000

General Errors:
- **405 Method Not Allowed:** The method is not allowed for the requsted URL.
- **404 Not Found:** The requested URL was not found on the server. 
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
- **Description:** Performs traceroute to test hops to the target.
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

### Key Logs - `/api/logs` - **This endpoint is intentionally vulnerable and reveals logged keys without authenticating the user to test possible API attacks in the future.**.

- **Method:** `GET`
- **Description:** Provides detailed logs of previously created keys.
- **Headers:** None required.
- **Request Body:** None required
- **Response:**
  ```json
  [
    {
        "api_key_hashed": "2286759824fa2972a9ef997525f373bdae488b9c68a81541f32fc4771dc16a71",
        "created_at": "2025-01-06 18:19:13.991751",
        "id": 1,
        "status": "inactive"
    },
    {
        "api_key_hashed": "e2c516d0ba2cebde56aaaaceff69e8d7ef8a5b846f6f95e5275182553bf2f50c",
        "created_at": "2025-01-06 18:49:04.072324",
        "id": 2,
        "status": "active"
    }
  ]

---

## 4. Testing with Postman

!Access Postman via the Desktop Agent!

To start testing with Postman we first need to generate a valid key that will grant us access to the other endpoints.

To generate the API-Key complete the following steps:

1. Open Postman Desktop Agent.
2. Select the method for the request, in this case `POST`.
3. Set the URL of the request to http://127.0.0.1:5000/api/key.
4. click "Send"
5. Observe the Body in the response and copy the generated api_key.

![image](https://github.com/user-attachments/assets/7881cc03-f2e9-4152-8ac0-00a90f36557e)

6. Refer to [API Endpoints](#3-api-endpoints) to check the settings required for each endpoint.
7. Click the Headers tab.
8. Add x-api-key in the Key column and your generated key in the Value column.
![image](https://github.com/user-attachments/assets/deee6232-b6d1-4850-88ba-bde3209479d6)


9. Make sure the header is enabled - Check the box next to the new header.
10. Set the Method and URI according to the API endpoint you want to use.
11. Depending on the endpoint used, you might need to include JSON data in the request body.
12. Observe the response Body for the returned data based on the call parameters.
