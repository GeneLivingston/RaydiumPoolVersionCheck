from solders.pubkey import Pubkey
from solana.rpc.api import Client

# Example usage with SOL-USDC pool
#pool_address = "8sLbNZoA1cfnvMJLPfp98ZLAnFSYCFApfJKMbiXNLwxj"
#result = inspect_pool_version(pool_address)

def inspect_pool_version(pool_address: str):
    try:
        # Initialize Solana RPC client
        client = Client("https://api.mainnet-beta.solana.com")
        pool_pubkey = Pubkey.from_string(pool_address)

        # Get pool account data
        pool_account = client.get_account_info(pool_pubkey)
        if pool_account.value is None:
            print("Pool not found")
            return None

        # Extract and convert version bytes to hex
        version_bytes = pool_account.value.data[:4]
        version_hex = version_bytes.hex()

        # Map of known version identifiers
        VERSION_IDENTIFIERS = {
            "f7ede3f5": "Version 4",
            "05953c85": "Version 3",
            "00000001": "Version 2",
        }

        version = VERSION_IDENTIFIERS.get(version_hex, "Unknown")

        print(f"Version bytes (hex): {version_hex}")
        print(f"Pool version: {version}")

        return version_hex, version
    except Exception as e:
        print(f"Error: {str(e)}")
        return None



