

def decode_host_info(host_info) -> list:
    """Decodes host information (host or (host, port)) and returns (host, port).
    This function takes a host information argument, which can be either a string
    representing the hostname/IP address or a tuple/list containing the 
    hostname/IP and the port number.  It decodes this information and returns
    the hostname/IP and port as a tuple.  If only the hostname/IP is provided,
    the default SSH port (22) is used.

    Args:
        host_info (str, tuple, or list): Hostname/IP (string) or a tuple/list
            containing (hostname/IP, port).

    Returns:
        tuple: A tuple containing the hostname/IP (str) and the port number (int).

    Raises:
        ValueError: If `host_info` is invalid. This can occur if:
            - `host_info` is a tuple or list, but it does not contain exactly two elements.
            - `host_info` is not a string, tuple, or list.
    """
    if isinstance(host_info, (tuple, list)):
        if len(host_info) != 2:  # Ensure tuple/list has exactly two elements
            raise ValueError(f"Invalid host info (tuple/list): {host_info}")
        host, port = host_info
    elif isinstance(host_info, str):
        host = host_info
        port = 22
    else:
        raise ValueError(f"Invalid host info type: {type(host_info)}")

    return host, port
