import asyncio
import logging
import os
from typing import Dict, List
from shared.api_client import get_linora_config
from utils import (
    generate_linora_account,
    get_l1_eth_account,
)

linora_http_url = "https://api.testnet.linora.trade/v1"
async def main(eth_private_key_hex: str) -> None:
    # Initialize Ethereum account
    _, eth_account = get_l1_eth_account(eth_private_key_hex)

    # Load linora config
    linora_config = await get_linora_config(linora_http_url)

    # Generate linora account (only local)
    linora_account_address, linora_account_private_key_hex = generate_linora_account(
        linora_config, eth_account.key.hex()
    )
    print(f"linora Account Address: {linora_account_address}")
    print(f"linora Account Private Key: {linora_account_private_key_hex}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO"),
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Load environment variables
    eth_private_key_hex = os.getenv('ETHEREUM_PRIVATE_KEY', "")
    asyncio.run(main(eth_private_key_hex))
