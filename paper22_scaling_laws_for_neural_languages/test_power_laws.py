"""
Core Paper:
    - Scaling Laws for Neural Language Models
Related Reading:
    - The Asethetics of randomness nassim taleb black swarm
    - M.EJ Newman(2005)
    - Scaling Laws, Carefully, Lilian Weng
"""



def power_law(x, alpha, b, c):
    """
    Output of this funciton is loss

    alpha_exponent for paramters, datasize and compute

    alpha_N = 0.076
    alpha_D = 0.095
    alpha_C = 0.050

    Notice these exponents are very small, way smaller than returns in financial markets
    alpha = 2 ~ 3 or even intensity of wars 0.8 and frequency of word use 1.2
    
    Critical parameter count
    Nc = 8.8e13 parameter count(human brain 8.6e10)
    Dc = 5.4e13
    Cc = 3,1e18 critical compute
    
    """
    return b * x ** (-alpha) + c

if __name__ == "__main__":
    assert power_law(1, 2, 2, 2) == 4