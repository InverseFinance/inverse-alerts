from utils.fetchers import getBalancerVaultBalances
from utils.helpers import getWeb3

web3=getWeb3(1)
test = getBalancerVaultBalances("0x5b3240b6be3e7487d61cd1afdfc7fe4fa1d81e6400000000000000000000037b")
print(test)