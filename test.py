import fetchers
from utils import formatCurrency

print(fetchers.getENS('0xfda9365e2cdf21d72cb0dc4f5ff46f29e4ac59ce'))
print(formatCurrency(fetchers.getBalance('0xfda9365e2cdf21d72cb0dc4f5ff46f29e4ac59ce','0x865377367054516e17014ccded1e7d814edc9ce4')))
print(fetchers.getName('0x865377367054516e17014ccded1e7d814edc9ce4'))
print(fetchers.getSymbol('0x865377367054516e17014ccded1e7d814edc9ce4'))
print(formatCurrency(fetchers.getSupply('0x865377367054516e17014ccded1e7d814edc9ce4')))
fetchers.getCash('0x7fcb7dac61ee35b3d4a51117a7c58d53f0a8a670')

