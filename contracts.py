contracts = {
    1: {
        "name": "DOLAFRAXBP Pool",
        "address": "0xE57180685E3348589E9521aa53Af0BCD497E884d",
        "alerts": {"events": ['curve_liquidity'],
                   "state": ['supply'],
                   "tx": []},
        "chain_ids": [1]
    },
    2: {
        "name": "DOLA-3CRV",
        "address": "0xaa5a67c256e27a5d80712c51971408db3370927d",
        "alerts": {"events": ['curve_liquidity'],
                   "state": ['supply'],
                   "tx": []},
        "chain_ids": [1]
    },
    3: {
        "name": "Debt Converter",
        "address": "0x1ff9c712B011cBf05B67A6850281b13cA27eCb2A",
        "alerts": {"events": ['debt_conversion'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    4: {
        "name": "Debt Repayer",
        "address": "0x9eb6BF2E582279cfC1988d3F2043Ff4DF18fa6A0",
        "alerts": {"events": ['debt_repayment'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    5: {
        "name": "Anchor Fed",
        "address": "0x5E075E40D01c82B6Bf0B0ecdb4Eb1D6984357EF7",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    7: {
        "name": "FtmChainFed",
        "address": "0x4d7928e993125a9cefe7ffa9ab637653654222e2",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1,250]
    },
    8: {
        "name": "Yearn Fed",
        "address": "0xcc180262347f84544c3a4854b87c34117acadf94",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    9: {
        "name": "Convex Fed",
        "address": "0x57D59a73CDC15fe717D2f1D433290197732659E2",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    10: {
        "name": "FusePool127Fed",
        "address": "0x5fa92501106d7e4e8b4ef3c4d08112b6f306194c",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    11: {
        "name": "FusePool22Fed",
        "address": "0x7765996dae0cf3ecb0e74c016fcdff3f055a5ad8",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    12: {
        "name": "FusePool24Fed",
        "address": "0xcbf33d02f4990babcba1974f1a5a8aea21080e36",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    13: {
        "name": "FusePool6Fed",
        "address": "0xe3277f1102c1ca248ad859407ca0cbf128db0664",
        "alerts": {"events": ['fed'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    14: {
        "name": "Curve Gauge Controller",
        "address": "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB",
        "alerts": {"events": ['gauge_controller'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    16: {
        "name": "GovernorMills",
        "address": "0xbeccb6bb0aa4ab551966a7e4b97cec74bb359bf6",
        "alerts": {"events": ['governance'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    17: {
        "name": "XINV",
        "address": "0x1637e4e9941d55703a7a5e7807d6ada3f7dcd61b",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    18: {
        "name": "anYvCrvDOLA ",
        "address": "0x3cFd8f5539550cAa56dC901f09C69AC9438E0722",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    19: {
        "name": "anYvDAI ",
        "address": "0xD79bCf0AD38E06BC0be56768939F57278C7c42f7",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    20: {
        "name": "anYvUSDT ",
        "address": "0x4597a4cf0501b853b029cE5688f6995f753efc04",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    21: {
        "name": "anYvUSDC ",
        "address": "0x7e18AB8d87F3430968f0755A623FB35017cB3EcA",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    22: {
        "name": "anyvYFI",
        "address": "0xE809aD1577B7fF3D912B9f90Bf69F8BeCa5DCE32",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    23: {
        "name": "anyvWETH",
        "address": "0xD924Fc65B448c7110650685464c8855dd62c30c0",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    24: {
        "name": "anyvcrvcvxeth",
        "address": "0xa6F1a358f0C2e771a744AF5988618bc2E198d0A0",
        "alerts": {"events": ['lending1'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    25: {
        "name": "anStETH",
        "address": "0xeA0c959BBb7476DDD6cD4204bDee82b790AA1562",
        "alerts": {"events": ['lending1'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    26: {
        "name": "anDOLA",
        "address": "0x7fcb7dac61ee35b3d4a51117a7c58d53f0a8a670",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    27: {
        "name": "anXSUSHI",
        "address": "0xd60b06b457bff7fc38ac5e7ece2b5ad16b288326",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    28: {
        "name": "anWBTC",
        "address": "0x17786f3813e6ba35343211bd8fe18ec4de14f28b",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": [],
                   "tx": ['cash']},
        "chain_ids": [1]
    },
    29: {
        "name": "anYFI",
        "address": "0xde2af899040536884e062d3a334f2dd36f34b4a4",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    30: {
        "name": "anETH",
        "address": "0x697b4acaa24430f254224eb794d2a85ba1fa1fb8",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    31: {
        "name": "anWBTCv2",
        "address": "0xE8A2eb30E9AB1b598b6a5fc4aa1B80dfB6F90753",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    32: {
        "name": "anETHv2",
        "address": "0x8e103Eb7a0D01Ab2b2D29C91934A9aD17eB54b86",
        "alerts": {"events": ['lending1', 'lending2'],
                   "state": ['cash'],
                   "tx": []},
        "chain_ids": [1]
    },
    33: {
        "name": "fAPE-127",
        "address": "0x8d68d8301fe02654791e6ef5e9ec240865bb79cd",
        "alerts": {"events": ['lendingfuse127'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    34: {
        "name": "fETH-127",
        "address": "0x26267e41ceca7c8e0f143554af707336f27fa051",
        "alerts": {"events": ['lendingfuse127'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    35: {
        "name": "ftUSD-127",
        "address": "0xf138c6f8832e405a35391fa3ef62a4b27299f2d4",
        "alerts": {"events": ['lendingfuse127'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    36: {
        "name": "fDOLA-127",
        "address": "0xc1fb01415f08fbd71623aded6ac8ec74f974fdc1",
        "alerts": {"events": ['lendingfuse127'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    37: {
        "name": "Oracle Inverse",
        "address": "0xe8929afd47064efd36a7fb51da3f8c5eb40c4cb4",
        "alerts": {"events": [],
                   "state": ['oracle'],
                   "tx": []},
        "chain_ids": [1]
    },
    38: {
        "name": "Analytics Multisig",
        "address": "0x49bb4559e65fc5f2236780079265d2f8f4f75c03",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    39: {
        "name": "Treasury Multisig",
        "address": "0x9d5df30f475cea915b1ed4c0cca59255c897b61b",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    40: {
        "name": "Policy Committee Multisig",
        "address": "0x4b6c63e6a94ef26e2df60b89372db2d8e211f1b7",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    41: {
        "name": "Growth Multisig",
        "address": "0x07de0318c24d67141e6758370e9d7b6d863635aa",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    42: {
        "name": "Community Multisig",
        "address": "0xa40fbd692350c9ed22137f97d64e6baa4f869e8c",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    43: {
        "name": "Bug Bounty Multisig",
        "address": "0x943dbdc995add25a1728a482322f9b3c575b16fb",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    44: {
        "name": "Fed Chair Multisig",
        "address": "0x8f97cca30dbe80e7a8b462f1dd1a51c32accdfc8",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [1]
    },
    45: {
        "name": "Fuse Pool 127 Unitroller",
        "address": "0x3f2d1bc6d02522dbcdb216b2e75edddafe04b16f",
        "alerts": {"events": [],
                   "state": ['liquidation_incentive'],
                   "tx": []},
        "chain_ids": [1]
    },
    46: {
        "name": "Fuse Pool 22 Unitroller",
        "address": "0xe3952d770fb26cc61877cd34fbc3a3750881e9a1",
        "alerts": {"events": [],
                   "state": ['liquidation_incentive'],
                   "tx": []},
        "chain_ids": [1]
    },
    47: {
        "name": "Fuse Pool 6 Unitroller",
        "address": "0x814b02c1ebc9164972d888495927fe1697f0fb4c",
        "alerts": {"events": [],
                   "state": ['liquidation_incentive'],
                   "tx": []},
        "chain_ids": [1]
    },
    48: {
        "name": "Optimism Treasury Multisig",
        "address": "0xa283139017a2f5BAdE8d8e25412C600055D318F8",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [10]
    },
    49: {
        "name": "Fantom Treasury Multisig",
        "address": "0x7f063F7B7A1326eE8B64ACFdc81Bf544ecc974bC",
        "alerts": {"events": [],
                   "state": [],
                   "tx": ['multisig']},
        "chain_ids": [250]
    },
    50: {
        "name": "Sushiswap INV/DOLA",
        "address": "0x5ba61c0a8c4dcccc200cd0ccc40a5725a426d002",
        "alerts": {"events": ['swap'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    51: {
        "name": "Sushiswap INV/WETH",
        "address": "0x328dfd0139e26cb0fef7b0742b49b0fe4325f821",
        "alerts": {"events": ['swap'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    52: {
        "name": "Uniswap INV/DOLA",
        "address": "0xb268C1c44a349D06a42cf24988162DADc48D839e",
        "alerts": {"events": ['swap'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    53: {
        "name": "DOLA",
        "address": "0x865377367054516e17014CcdED1e7d814EDC9ce4",
        "alerts": {"events": ['concave'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    54: {
        "name": "3CRV",
        "address": "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490",
        "alerts": {"events": ['concave'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    55: {
        "name": "Anchor Unitroller",
        "address": "0x4dcf7407ae5c07f8681e1659f626e114a7667339",
        "alerts": {"events": ['unitroller'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    56: {
        "name": "StrategyConvex3CRV",
        "address": "0x64e4fC597C70B26102464B7F70B1F00C77352910",
        "alerts": {"events": ['harvest'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    57: {
        "name": "ssc_DOLA_DOLA_U",
        "address": "0x00Ca07f4012dEbb0BD17cF15B1C2841928Da0484",
        "alerts": {"events": ['harvest'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    58: {
        "name": "USDC",
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "alerts": {"events": ['transf_usdc', 'profits'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    59: {
        "name": "DAI",
        "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "alerts": {"events": ['profits'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    60: {
        "name": "CRV",
        "address": "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "alerts": {"events": ['profits'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    },
    61: {
        "name": "Convex",
        "address": "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
        "alerts": {"events": ['profits'],
                   "state": [],
                   "tx": []},
        "chain_ids": [1]
    }
}

collaterals_v1 = {"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":"0x697b4acAa24430F254224eB794d2a85ba1Fa1FB8",
               "0x865377367054516e17014CcdED1e7d814EDC9ce4":"0x7Fcb7DAC61eE35b3D4a51117A7c58D53f0a8a670",
               "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272":"0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272",
               "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599":"0xE8A2eb30E9AB1b598b6a5fc4aa1B80dfB6F90753",
               "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e":"0xde2af899040536884e062D3a334F2dD36F34b4a4"}
