def splitPair(pair):
    if pair.endswith('USDT') or pair.endswith('USDC'):
        base =  pair[:-4]
        quote = pair[-4:]
        return base,quote
