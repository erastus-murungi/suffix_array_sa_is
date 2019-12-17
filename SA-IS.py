from array import array

L_TYPE = ord('L')
S_TYPE = ord('S')
SIGMA = 256


def is_lms(i, t):
    return t[i] == S_TYPE and t[i - 1] == L_TYPE


def ranks(text, n):
    pass


def print_(data: bytearray):
    print(data.decode('ascii'))
    print("".join(
        "^" if is_lms(i, data) else " "
        for i in range(len(data))
    ))


def classify(text, n):
    t = bytearray(n)
    t[-1] = S_TYPE
    for i in range(n - 2, -1, -1):
        if text[i] == text[i + 1]:
            t[i] = t[i + 1]
        else:
            if text[i] > text[i + 1]:
                t[i] = L_TYPE
            else:
                t[i] = S_TYPE
    return t


def find_lms_suffixes(t, n):
    pos = array('l')
    for i in range(n - 1, 0, -1):
        if t[i] == S_TYPE and t[i - 1] == L_TYPE:
            pos.append(i)
    return pos


def print_buckets(bucks):
    res = '[ '
    for b in bucks:
        if b != 0:
            res += str(b)
            res += ' '
    res += ']'
    print(res)


def buckets(text):
    alpha = bytearray()
    bucket_sizes = array('L', [0] * SIGMA)
    for c in text:

        bucket_sizes[c] += 1
    for i in range(SIGMA):
        if bucket_sizes[i] != 0:
            alpha.append(i)

    # print_buckets(bucket_sizes)
    return alpha, bucket_sizes


def bucket_intervals(alpha, bucket_sizes):
    heads = array('l', [0] * SIGMA)
    tails = array('l', [0] * SIGMA)
    j = 0
    for i in range(len(alpha)):
        heads[alpha[i]] = j
        j += bucket_sizes[alpha[i]]
        tails[alpha[i]] = j - 1

    # print_buckets(heads)
    # print_buckets(tails)
    return heads, tails


def induced_sorting(lms, tails, heads, SA, type_suffix, text, n, alpha, bucket_sizes):
    for s in lms:  # place LMS suffixes at the end of their buckets
        nfs = tails[text[s]]
        SA[nfs] = s
        tails[text[s]] -= 1

    for i in range(n):  # place the L-type suffixes at the fronts of their buckets
        if SA[i] > 0 and type_suffix[SA[i] - 1] == L_TYPE:
            nfs = heads[text[SA[i] - 1]]
            SA[nfs] = SA[i] - 1
            heads[text[SA[i] - 1]] += 1

    # reset bucket counters
    heads, tails = bucket_intervals(alpha, bucket_sizes)

    for i in range(n-1, -1, -1):  # place the S-type suffixes at the ends of their buckets
        if SA[i] > 0 and type_suffix[SA[i] - 1] == S_TYPE:
            nfs = tails[text[SA[i] - 1]]
            SA[nfs] = SA[i] - 1
            tails[text[SA[i] - 1]] -= 1


def blocks_are_equal(i, j, types, text, n):
    while i < n and j < n:
        if text[i] == text[j]:
            if is_lms(i, types) and is_lms(j, types):
                return True
            else:
                i += 1
                j += 1
        else:
            return False
    return False


def get_reduced_substring(types, SA, lms, ordered_lms, text, n, m):
    j = 0
    for i in range(n):
        if is_lms(SA[i], types):
            ordered_lms[j] = SA[i]
            j += 1

    # number the lms blocks and form the reduced substring
    pIS = array('l', [0] * m)
    k, i = 1, 1
    pIS[0] = 0
    for i in range(1, m):
        if text[ordered_lms[i]] == text[ordered_lms[i - 1]] and \
                blocks_are_equal(ordered_lms[i] + 1, ordered_lms[i - 1] + 1, types, text, n):
            pIS[i] = pIS[i - 1]
        else:
            pIS[i] = k
            k += 1

    # form the reduced substring
    ipIS = array('i', [0] * SIGMA)
    for i in range(m):
        ipIS[text[ordered_lms[i]]] = pIS[i]
    for i in range(m):
        pIS[i] = ipIS[text[lms[i]]]

    pIS.reverse()
    print(pIS)
    return pIS, k == m


def suffix_array(T, SA):
    n = len(T)
    t = classify(T, n)

    lms = find_lms_suffixes(t, n)
    m = len(lms)

    print_(t)

    alpha, sizes = buckets(T)

    heads, tails = bucket_intervals(alpha, sizes)
    induced_sorting(lms, tails, heads, SA, t, T, n, alpha, sizes)   # first induced sort

    ordered_lms = array('L', [0] * len(lms))

    reduced_ST, blocks_unique = get_reduced_substring(t, SA, lms, ordered_lms, T, n, m)
    SA_reduced = array('l', [-1] * m)
    if blocks_unique:  # base case
        # compute suffix array manually
        for i in range(m):
            SA_reduced[reduced_ST[i]] = i
    else:
        suffix_array(reduced_ST, SA_reduced)
        # use the suffix array to sort the LMS suffixes
        for i in range(m):
            lms[i] = ordered_lms[SA_reduced[i]]

        induced_sorting(lms, tails, heads, SA, t, T, n, alpha, sizes)


if __name__ == '__main__':
    T = 'GTCCCGATGTCATGTCAGGA'
    T += '$'
    T = [ord(c) for c in T]
    n = len(T)
    SA = array('l', [-1] * n)

    suffix_array(T, SA)

