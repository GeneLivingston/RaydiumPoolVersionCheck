# RaydiumPoolVersionCheck
Determines the version of a Raydium pool (necessary for interpreting pool info)

## A Guide to Raydium Pool Versions

This guide explains how to determine the version of a Raydium liquidity pool on Solana. Understanding pool versions is crucial because different versions have different data layouts and features.

## Background

Raydium pools have evolved over time, with different versions using different data structures. The version number is encoded in the first 4 bytes of the pool's account data. This information is critical because:
1. Different versions store data at different offsets
2. Fee structures might vary between versions
3. Feature sets can be different
4. Integration code needs to handle each version appropriately

## Known Version Identifiers

```
Version 2: 00000001
Version 3: 05953c85
Version 4: f7ede3f5
```

Version 4 is currently the most common version for active pools. 
Version 5 does exist, but I do not know the identifier for them.

## Implementation

Here's a Python script that determines a Raydium pool's version:

```python
from solders.pubkey import Pubkey
from solana.rpc.api import Client

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

# Example usage with SOL-USDC pool
pool_address = "8sLbNZoA1cfnvMJLPfp98ZLAnFSYCFApfJKMbiXNLwxj"
result = inspect_pool_version(pool_address)



## Common Challenges and Solutions

### 1. Async/Await Complexity

**Challenge**: The Solana RPC client libraries have undergone changes in how they handle async operations. Some versions use async/await patterns while others don't.

**Solution**: The current implementation uses synchronous calls for simplicity and compatibility. If you need async functionality, you'll need to modify the code based on your specific library versions.

### 2. RPC Node Reliability

**Challenge**: Public RPC nodes can be unreliable or rate-limited.

**Solution**: 
- Use a reliable RPC endpoint
- Implement retry logic if needed
- Consider running your own RPC node for production use

```python
# Example with retry logic
def get_account_with_retry(client, pubkey, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.get_account_info(pubkey)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1 * (attempt + 1))
```

### 3. Version Detection Edge Cases

**Challenge**: New pool versions might be deployed, or you might encounter custom pools.

**Solution**: The code includes an "Unknown" version handler and logs the hex value for investigation:

```python
version = VERSION_IDENTIFIERS.get(version_hex, "Unknown")
if version == "Unknown":
    print(f"Warning: Unknown version identifier: {version_hex}")
```

### 4. Data Format Issues

**Challenge**: The binary data needs to be properly converted to hex.

**Solution**: Use proper byte ordering and hex conversion:
```python
version_bytes = pool_account.value.data[:4]
version_hex = version_bytes.hex()  # Proper hex conversion
```

## Usage Notes

0. **Requirements: import the dependencies before using this script

    $ pip install -r requirements.txt

    then in your script...

    from raydium_bot.tools.raydiumpoolversion import *


1. **Pool Address Format**: Make sure to use the correct pool address format. Raydium pool addresses are base-58 encoded strings.

2. **Error Handling**: The script includes basic error handling, but you might want to add more specific handling for your use case.

3. **Version-Specific Logic**: Once you know the pool version, you'll need version-specific code to handle the pool's data layout.

## Example Pool Data Layouts

Different versions store data at different offsets. Here's a basic overview:

### Version 4 Layout
```
Offset  Length  Description
0       4       Version identifier (f7ede3f5)
96      32      Base token vault address
128     32      Quote token vault address
160     8       Base token reserve
168     8       Quote token reserve
176     2       Fee rate
```

### Version 3 Layout
```
Offset  Length  Description
0       4       Version identifier (05953c85)
// Different layout - consult documentation
```

## Testing Different Pools

You can test different pools by changing the pool_address:

```python
# Some example pools
SOL_USDC = "8sLbNZoA1cfnvMJLPfp98ZLAnFSYCFApfJKMbiXNLwxj"
BONK_SOL = "Dq5C6ha9qkscrYe8RUVx5ptD9YzqGx2piR7V7mcxS2XL"
USDT_USDC = "2EXiumdi14E9b8Fy62QcA5Uh6WdHS2b38wtSxp72Mibj"

# Test each pool
from raydium_bot.tools.raydiumpoolversion import *
for pool in [SOL_USDC, BONK_SOL, USDT_USDC]:
    print(f"\nChecking pool: {pool}")
    inspect_pool_version(pool)
```

## Future Improvements

1. Add support for new versions as they're released
2. Implement caching for frequently checked pools
3. Add detailed pool information based on version
4. Include pool status checking
5. Add support for custom RPC endpoints

## Additional Resources

1. [Raydium Documentation](https://docs.raydium.io/)
2. [Solana Documentation](https://docs.solana.com/)
3. [Raydium GitHub](https://github.com/raydium-io/raydium-sdk)

Remember to always test with mainnet-fork or devnet before deploying to production, and handle version-specific features appropriately in your application.
