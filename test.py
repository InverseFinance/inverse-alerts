from utils import getUnderlyingPrice
from utils import getDecimals
from utils import getSupply,getCash,getBalance,getName,getTx

#print(getUnderlyingPrice('0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272','0xe8929afd47064efd36a7fb51da3f8c5eb40c4cb4'))
#print(getDecimals('0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272'))
#print("{:,.2f}".format(getSupply('0x7fcb7dac61ee35b3d4a51117a7c58d53f0a8a670')))

print(getName('0x865377367054516e17014ccded1e7d814edc9ce4'))
print("{:,.2f}".format(getBalance('0xfda9365e2cdf21d72cb0dc4f5ff46f29e4ac59ce','0x865377367054516e17014ccded1e7d814edc9ce4')))
#print("{:,.2f}".format(getCash('0x7fcb7dac61ee35b3d4a51117a7c58d53f0a8a670')))
print(getTx('0xb917c9ed47a1235c2b09d5a2e057d22140b94b34e7b2062d14296d044b8db716'))

