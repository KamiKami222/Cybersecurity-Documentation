import sqlite3
import secrets
import hashlib
import subprocess
import socket
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)


# Database connection helpers
def connect_logs_db():
    return sqlite3.connect("logs.db")


def connect_internal_db():
    return sqlite3.connect("internal.db")


# Hashing helper function
def hash_api_key(api_key):
    """Hash the API key using SHA-256."""
    return hashlib.sha256(api_key.encode()).hexdigest()


# Initialize databases
def initialize_databases():
    # Create visible database (logs.db)
    with connect_logs_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS api_key_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key_hashed TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        );
        """)

    # Create internal database (internal.db)
    with connect_internal_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS internal_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key_hashed TEXT NOT NULL UNIQUE
        );
        """)


# Generate a new API key
@app.route('/api/key', methods=['POST'])
def generate_new_key():
    # Generate a new API key
    api_key = secrets.token_urlsafe(32)
    api_key_hashed = hash_api_key(api_key)
    created_at = datetime.now()

    # Deactivate all existing keys in logs.db
    with connect_logs_db() as conn:
        conn.execute("UPDATE api_key_logs SET status = 'inactive'")

    # Insert the new key as active in logs.db
    with connect_logs_db() as conn:
        conn.execute(
            "INSERT INTO api_key_logs (api_key_hashed, created_at, status) VALUES (?, ?, 'active')",
            (api_key_hashed, created_at)
        )

    # Replace the key in internal.db
    with connect_internal_db() as conn:
        conn.execute("DELETE FROM internal_keys")  # Clear the internal keys
        conn.execute(
            "INSERT INTO internal_keys (api_key_hashed) VALUES (?)",
            (api_key_hashed,)
        )

    return jsonify({"message": "New API key generated.", "api_key": api_key})


# Validate API key
def validate_api_key(provided_key):
    """Check if the provided API key is valid."""
    provided_key_hashed = hash_api_key(provided_key)

    with connect_internal_db() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM internal_keys WHERE api_key_hashed = ?",
            (provided_key_hashed,)
        )
        return cursor.fetchone() is not None


# DNS Lookup Function
def dns_lookup(domain):
    """Perform DNS lookup for a given domain."""
    try:
        ip = socket.gethostbyname(domain)
        return {"domain": domain, "ip": ip}
    except socket.gaierror:
        return {"error": "Unable to resolve domain"}


# Traceroute Function
def traceroute(target):
    """Perform traceroute using the Windows tracert command."""
    try:
        result = subprocess.run(
            ["tracert", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        return str(e)


# Ping Function
def ping(target):
    """Perform a ping using the Windows ping command."""
    try:
        result = subprocess.run(
            ["ping", "-n", "1", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        return str(e)


# DNS Lookup Endpoint
@app.route('/api/dns', methods=['POST'])
def api_dns():
    api_key = request.headers.get('x-api-key')
    if not validate_api_key(api_key):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    domain = data.get("domain")
    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    result = dns_lookup(domain)
    return jsonify(result)


# Traceroute Endpoint
@app.route('/api/traceroute', methods=['POST'])
def api_traceroute():
    api_key = request.headers.get('x-api-key')
    if not validate_api_key(api_key):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    target = data.get("target")
    if not target:
        return jsonify({"error": "Target is required"}), 400

    result = traceroute(target)
    return jsonify({"target": target, "result": result})


# Updated Ping Endpoint
@app.route('/api/ping', methods=['POST'])
def api_ping():
    api_key = request.headers.get('x-api-key')
    if not validate_api_key(api_key):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    target = data.get("target")
    if not target:
        return jsonify({"error": "Target is required"}), 400

    result = ping(target)
    return jsonify({"target": target, "result": result})


# View logs (Visible database)
@app.route('/api/logs', methods=['GET'])
def view_logs():
    with connect_logs_db() as conn:
        cursor = conn.execute("SELECT * FROM api_key_logs")
        logs = [
            {"id": row[0], "api_key_hashed": row[1], "created_at": row[2], "status": row[3]}
            for row in cursor.fetchall()
        ]
    return jsonify(logs)


# Initialize databases at app startup
initialize_databases()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
