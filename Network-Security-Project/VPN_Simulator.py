"""
This program simulates a basic VPN/proxy connection demo.  
It shows your real IP address and allows you to “connect” to fake VPN IPs from different countries.
"""

import requests


# ------------------- Fake VPN IPs -------------------

vpn_servers = {
    "United States": "104.28.45.19",
    "United Kingdom": "81.23.56.99",
    "Germany": "91.12.84.201",
    "Japan": "150.95.23.77",
    "Brazil": "177.67.89.45",
    "Canada": "142.112.66.10",
    "Australia": "203.44.12.98"
}


# ------------------- Get Real IP -------------------

def fetch_real_ip():
    """Get your real public IP address using an API."""
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=5)
        return resp.json().get("ip")
    except Exception as e:
        return f"Error: {e}"


# ------------------- VPN Demo -------------------

def vpn_demo():
    """Show a demo of connecting to fake VPN IPs."""
    print("Simple VPN/Proxy Demo")

    # Display real IP
    real_ip = fetch_real_ip()
    print(f"Your Real IP: {real_ip}\n")

    # Show list of available VPN locations
    print("Choose a VPN server location:")
    for idx, country in enumerate(vpn_servers.keys(), start=1):
        print(f"{idx}. {country}")

    # Ask user to select a country
    choice = input("\nEnter the number of your chosen country: ")

    try:
        choice = int(choice)
        country = list(vpn_servers.keys())[choice - 1]
        fake_ip = vpn_servers[country]

        print(f"\nConnecting to VPN server in {country}...")
        print(f"Your new (simulated) IP: {fake_ip}")

    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")


# ------------------- Run Program -------------------

if __name__ == "__main__":
    vpn_demo()