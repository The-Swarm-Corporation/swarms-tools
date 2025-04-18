from swarms_tools.finance.check_solana_address import (
    check_solana_balance,
    check_multiple_wallets,
)

print(
    check_solana_balance(
        "7MaX4muAn8ZQREJxnupm8sgokwFHujgrGfH9Qn81BuEV"
    )
)
print(
    check_multiple_wallets(
        [
            "7MaX4muAn8ZQREJxnupm8sgokwFHujgrGfH9Qn81BuEV",
            "7MaX4muAn8ZQREJxnupm8sgokwFHujgrGfH9Qn81BuEV",
        ]
    )
)
