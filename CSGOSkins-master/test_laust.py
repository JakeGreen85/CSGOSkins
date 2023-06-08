from bank.models import select_assets

print(select_assets()[0].price)