import paramiko
import socket
import concurrent.futures
import re

from utils import decode_host_info


def check_db_running(host_info, username="root", certificate_path=None, db_type="mysql"):  # Added db_type
    """Checks if MySQL or MariaDB is running on a host via SSH.

    Args:
        host_info (str, tuple, or list): Hostname/IP or (hostname/IP, port). Port is optional.
        username (str, optional): Username for SSH. Defaults to "root".
        certificate_path (str, optional): Path to SSH certificate. Defaults to None.
        db_type (str, optional): "mysql" or "mariadb". Defaults to "mysql".

    Returns:
        str: Status of the database server.
    """
    host, port = decode_host_info(host_info)

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if certificate_path:
            try:
                client.connect(host, port=port, username=username, key_filename=certificate_path, timeout=10)
            except paramiko.AuthenticationException:
                return f"{host}:{port}: Authentication failed (certificate)"
            except (socket.gaierror, TimeoutError) as e:
                return f"{host}:{port}: Connection error: {e}"
            except Exception as e:
                return f"{host}:{port}: SSH error: {e}"
        else:
            return f"{host}:{port}: Certificate path is required"

        # Check systemd for MySQL/MariaDB
        service_name = f"{db_type}d"  # mysql or mariadbd
        stdin, stdout, stderr = client.exec_command(f"systemctl is-active {service_name}")
        db_status = stdout.read().decode().strip()

        if db_status == "active":
            client.close()
            return f"{host}:{port}: {db_type.capitalize()} is running"


        # Check for older init scripts (less reliable)
        stdin, stdout, stderr = client.exec_command(f"service {db_type} status")
        alt_status = stdout.read().decode().strip()

        if re.search(r"is running", alt_status, re.IGNORECASE):
            client.close()
            return f"{host}:{port}: {db_type.capitalize()} is running (SysV init)"


        client.close()
        return f"{host}:{port}: {db_type.capitalize()} is NOT running (or not found)"

    except Exception as e:
        return f"{host}:{port}: Error: {e}"


def main():
    hosts_with_ports = [
        "192.168.101.233",  # Just the hostname (port 22 assumed)
        ("192.168.112.6", 2222),  # Host and port
        # ... more hosts (with or without ports)
    ]
    username = "root"
    certificate_path = "/root/.ssh/id_rsa"
    db_types = ["mariadb", "mysql"]  # must have one entry of each host in hosts_with_ports

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(check_db_running, host_info, username, certificate_path, db_type)
            for host_info, db_type in zip(hosts_with_ports, db_types)
        ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)


if __name__ == "__main__":
    main()