import asyncio
import logging
import os
import traceback

import aiohttp
from shared.api_client import get_linora_config
from onboarding import get_jwt_token, get_open_orders, perform_onboarding
from utils_hd import generate_linora_account_from_ledger

linora_http_url = "https://api.testnet.linora.trade/v1"


async def main(eth_account_address: str) -> None:
    # Load linora config
    linora_config = await get_linora_config(linora_http_url)

    # Generate linora account (from ledger)
    linora_account_address, linora_account_private_key_hex = generate_linora_account_from_ledger(
        linora_config, eth_account_address
    )

    # Onboard generated linora account
    logging.info("Onboarding...")
    await perform_onboarding(
        linora_config,
        linora_http_url,
        linora_account_address,
        linora_account_private_key_hex,
        eth_account_address,
    )

    # Get a JWT token to interact with private endpoints
    logging.info("Getting JWT...")
    linora_jwt = await get_jwt_token(
        linora_config,
        linora_http_url,
        linora_account_address,
        linora_account_private_key_hex,
    )

    # Get account's open orders using the JWT token
    logging.info("Getting account's open orders...")
    open_orders = await get_open_orders(linora_http_url, linora_jwt)

    print(f"Open Orders: {open_orders}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO"),
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Load environment variables
    eth_account_address = os.getenv('ETHEREUM_ADDRESS', "")

    # Run main
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(eth_account_address))
    except Exception as e:
        logging.error("Local Main Error")
        logging.error(e)
        traceback.print_exc()
