"""
This program checks if a given URL is secure by validating that it uses HTTPS and has a valid SSL certificate.  
It reports whether the certificate is valid, expired, or if the connection is insecure.
"""

import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime


def verify_url_security(url: str) -> str:
    """
    Verify if the provided URL is secure by checking its scheme and SSL certificate.
    Returns a message describing the security status.
    """
    try:
        parsed = urlparse(url)
        scheme = parsed.scheme
        host = parsed.hostname

        if not scheme:
            return "Invalid URL: missing scheme (http/https)."
        if not host:
            return "Invalid URL: missing hostname."

        if scheme.lower() != "https":
            return "Insecure: connection uses HTTP (not encrypted)."

        # Establish SSL connection and fetch certificate
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host) as conn:
            conn.settimeout(5.0)
            conn.connect((host, 443))
            cert = conn.getpeercert()

        # Parse certificate expiry
        expiry_raw = cert.get("notAfter")
        expiry_date = datetime.strptime(expiry_raw, "%b %d %H:%M:%S %Y %Z")
        now = datetime.utcnow()

        if expiry_date < now:
            return f"SSL certificate expired on {expiry_date}."
        return f"Secure: valid SSL certificate (expires {expiry_date})."

    except ssl.SSLError:
        return "SSL error: invalid or untrusted certificate."
    except socket.timeout:
        return "Connection timed out: server unreachable."
    except Exception as e:
        return f"Unexpected error: {e}"


# ------------------- Main -------------------

if __name__ == "__main__":
    url = input("Enter a URL (e.g. https://example.com): ").strip()
    status = verify_url_security(url)
    print(status)
