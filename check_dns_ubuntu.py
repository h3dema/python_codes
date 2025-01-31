""" check if Bind DNS is running on remote servers.
    works on Ubuntu
"""
import paramiko
import socket
import concurrent.futures
import re

from utils import decode_host_info


def check_dns_running(host_info, username: str = "root", certificate_path=None):
    """Checks if Bind DNS server is running on a host via SSH.

    This function attempts to connect to the specified host via SSH using either certificate-based authentication.  
    It then checks the status of the Bind DNS service using systemd (for modern Ubuntu systems) and falls back
    to SysV init scripts for older systems.

    Args:
        host_info (tuple or list): A tuple or list containing the hostname/IP and port.
                                    e.g., ("example.com", 22) or ["192.168.1.100", 2222]
        username (str, optional): The username for SSH authentication. Defaults to "root".
        certificate_path (str): The path to the SSH certificate file.
            If provided, certificate authentication will be used.  If None, password
            authentication will be attempted (less secure).  Defaults to None.

    Returns:
        str: A string indicating the status of the Bind DNS server on the host.
            Possible return values include:
            - "{host_info}: Bind DNS is running"
            - "{host_info}: Bind DNS is running (SysV init)"  (for older systems)
            - "{host_info}: Bind DNS is NOT running (or not found)"
            - "{host_info}: Authentication failed (certificate)"
            - "{host_info}: Connection error: {error_message}"
            - "{host_info}: SSH error: {error_message}"
            - "{host_info}: Certificate path is required" (if no certificate path is given)
            - "{host_info}: Error: {error_message}" (for other errors)

    Raises:
        check decode_host_info()
    """
    host, port = decode_host_info(host_info)

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accept unknown host keys (use with caution)

        if certificate_path:
            try:
                client.connect(
                    host,
                    port=port,
                    username=username,
                    key_filename=certificate_path,
                    timeout=10  # Timeout for connection
                )
            except paramiko.AuthenticationException:
                return f"{host}:{port}: Authentication failed (certificate)"
            except (socket.gaierror, TimeoutError) as e:
                return f"{host}:{port}: Connection error: {e}"
            except Exception as e:
                return f"{host}:{port}: SSH error: {e}"

        else:  # Password authentication (less secure, avoid if possible)
            return f"{host}:{port}: Certificate path is required"

        # Check systemd status for Bind (works on Ubuntu 16.04+)
        stdin, stdout, stderr = client.exec_command("systemctl is-active bind9")  # Adjust service name if necessary

        dns_status = stdout.read().decode().strip()

        if dns_status == "active":
            client.close()
            return f"{host}:{port}: Bind DNS is running"

        # Check for older SysV init scripts (if systemd fails) – less reliable
        stdin, stdout, stderr = client.exec_command("service bind9 status")
        alt_status = stdout.read().decode().strip()

        if re.search(r"is running", alt_status, re.IGNORECASE): #Check if the string "is running" (case insensitive) is present in the output
            client.close()
            return f"{host}:{port}: Bind DNS is running (SysV init)"

        client.close()
        return f"{host}:{port}: Bind DNS is NOT running (or not found)"

    except Exception as e:
        return f"{host}:{port}: Error: {e}"


def main():
    hosts_with_ports  = [
        ("192.168.112.2", 22222),  # ip_or_hostname1, ssh port [optional]
        ("192.168.112.3", 22222),
        ("192.168.112.4", 22222),
        # ... more hosts
    ]
    username = "root"  # Or another user
    certificate_path = "/root/.ssh/id_rsa"  # Path to your SSH certificate

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(check_dns_running, host_info , username, certificate_path)
            for host_info in hosts_with_ports 
        ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)


if __name__ == "__main__":
    main()