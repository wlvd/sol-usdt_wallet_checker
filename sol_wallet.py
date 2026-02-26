from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.rpc.types import TokenAccountOpts
import time
import sys

from rich import print as rprint

from prompt_toolkit import prompt

def move_up(n):
    sys.stdout.write(f"\033[{n}F")
    sys.stdout.flush()

RPC = "https://api.mainnet-beta.solana.com"
USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
TOKEN_PROGRAM = PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

client = Client(RPC)

while True:
    wallet_string = prompt("Solana Wallet: ", placeholder="Public Key Required").strip()
    try:
        wallet = PublicKey(wallet_string)
        move_up(1)
        rprint(f"Valid Solana Wallet: [green]{wallet_string}[/green]")

        print("\n\n\n")

        opts = TokenAccountOpts(program_id=TOKEN_PROGRAM)

        while True:
            #SOL
            sol=0
            lamports = client.get_balance(wallet).value
            sol = lamports / 1_000_000_000

            #USDT
            usdt = 0.0
            resp = client.get_token_accounts_by_owner_json_parsed(wallet, opts)
            for acc in resp.value:
                info = acc.account.data.parsed["info"]
                if info["mint"] == USDT_MINT:
                    usdt = float(info["tokenAmount"]["uiAmountString"] or 0.0)


            for i in range(10, 0, -1):
                move_up(3)
                rprint(f"SOL: {sol}")
                rprint(f"USDT: {usdt}")
                rprint(f"[bright_black]Refreshing in {i} seconds...[/bright_black]")
                time.sleep(1)          
    except Exception:
        move_up(1)
        rprint(f"Invalid Solana Wallet: [red]{wallet_string}[/red]")