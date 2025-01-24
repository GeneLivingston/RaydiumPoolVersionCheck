from solana.rpc.api import Client
#from solana.publickey import PublicKey
#from solana import PublicKey
from solders.pubkey import Pubkey
from base58 import b58decode, b58encode


import json

def get_market_program_id(pool_address: str) -> Pubkey:
   bytes_address = b58decode(pool_address)
   client = Client("https://api.mainnet-beta.solana.com")
   resp = client.get_account_info(Pubkey(bytes_address))

   if hasattr(resp, 'value') and resp.value:
      raw_bytes = resp.value.data
      program_id_bytes = raw_bytes[:32]
      market_program_id = b58encode(program_id_bytes).decode()

      with open('info.txt', 'w') as f:
         f.write(str(market_program_id))
      return market_program_id

   else:
      data = resp['result']['value']['data'][0]
      decoded = json.loads(data)
      return Pubkey(decoded['marketProgramId'])


