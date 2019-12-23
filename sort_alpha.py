from array import array

def sort_alphabet_array(text):
    """Converts text to its corresponding integer alphabet representation"""
    sigma = 0
    for c in text:
        if ord(c) > sigma:
            sigma = ord(c)

    b = array('l', [0] * (sigma + 1))
    for c in text:
        b[ord(c)] = 1

    alpha = []
    for i in range(sigma + 1):
        if b[i]:
            alpha.append(i)

    w = {}
    r = 0
    R = array('l')
    for i in alpha:
        if i not in w:
            w[i] = r
            r += 1

    for c in text:
        R.append(w[ord(c)])

    return R, r
