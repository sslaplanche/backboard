FP_WEIGHTS = { 
    "pts": 1, 
    "reb": 1.2, 
    "ast": 1.5, 
    "stl": 3, 
    "blk": 3, 
    "tov": -1 
}

# Fantasy Points calculator
def fp(stats):
    f_stats = {k.lower(): v for k, v in stats.items()}
    weights = FP_WEIGHTS
    return round(sum([f_stats[key] * weights[key] for key in weights.keys()]), 2)