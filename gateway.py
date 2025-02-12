import netifaces

def get_default_gateway_netifaces():
    try:
        gateways = netifaces.gateways()
        # netifaces returns a dictionary, check for IPv4 and IPv6
        for family in [netifaces.AF_INET, netifaces.AF_INET6]:
            if family in gateways and gateways[family]:
                # Typically, the first entry is the default gateway
                gateway_ip = gateways[family][0][0]
                return gateway_ip
        return None
    except Exception as e:
        print(f"Error getting gateway: {e}")
        return None

gateway = get_default_gateway_netifaces()
if gateway:
    print(f"Default Gateway: {gateway}")
else:
    print("Default gateway not found.")
