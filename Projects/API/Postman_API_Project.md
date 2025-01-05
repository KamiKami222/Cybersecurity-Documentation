# Postman API Project

This project demonstrates building and testing an API using Flask, with Postman as the testing tool. The API supports network diagnostic tools like ping, DNS lookup, and traceroute, and is secured with API key authentication.

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
- **Postman**: Testing and debugging API requests.

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
