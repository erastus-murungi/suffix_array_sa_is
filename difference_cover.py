#!/usr/bin/env python
# -*- coding: utf-8 -*-
from array import array


def construct_suffix_array(s):
    n = len(s) + 1
    s += chr(36) * 4

    SA = array("l", [0 for _ in s])
    alpha = sorted(set(s))
    difference_cover(s, SA, n, alpha)
    return SA[:-3]
    # return array('l', [n]) + SA[:-3]


def difference_cover(s, SA, n, alpha):
    n0 = (n + 2) // 3
    n1 = (n + 1) // 3
    n2 = n // 3
    n02 = n0 + n2
    SA12 = [0] * (n02 + 3)
    SA0 = [0] * n0
    s12 = [i for i in range(n + (n0 - n1)) if i % 3 != 0]
    # substrings = sorted([s[i: i + 3] for i in s12])
    # print(substrings)

    s12.extend([0, 0, 0])

    radixpass(s12, SA12, s[2:], n02, alpha)  # sort using third character .. s + 2
    radixpass(SA12, s12, s[1:], n02, alpha)  # sort using second character .. s + 1
    radixpass(s12, SA12, s, n02, alpha)  # sort using first character .. s

    rank = 0
    c0, c1, c2 = -1, -1, -1
    arr = [0]  # rank of first suffix is 0
    for i in range(n02):
        if s[SA12[i]] != c0 or s[SA12[i] + 1] != c1 or s[SA12[i] + 2] != c2:
            rank += 1
            arr.append(rank)
            c0 = s[SA12[i]]
            c1 = s[SA12[i] + 1]
            c2 = s[SA12[i] + 2]

        if SA12[i] % 3 == 1:
            s12[SA12[i] // 3] = rank

        else:  # SA12[i] % 3 == 2
            s12[SA12[i] // 3 + n0] = rank

    # if the ranks are not unique, recurse on string s12, with SA=SA12, and alphabet = arr
    if rank < n02:
        difference_cover(s12, SA12, n02, arr)
        for i in range(n02):
            s12[SA12[i]] = i + 1
    else:
        for i in range(n02):
            SA12[s12[i] - 1] = i

    s0 = [SA12[i] * 3 for i in range(n02) if SA12[i] < n0]

    #  stably sort the mod 0 suffixes from SA12 by their first character
    radixpass(s0, SA0, s, n0, alpha)

    p = k = 0
    t = n0 - n1
    while k < n:
        i = SA12[t] * 3 + 1 if SA12[t] < n0 else (SA12[t] - n0) * 3 + 2

        #    j = p < n0 and SA0[p] or 0
        j = SA0[p] if p < n0 else 0

        if SA12[t] < n0:
            test = (
                (s12[SA12[t] + n0] <= s12[j // 3]) if (s[i] == s[j]) else (s[i] < s[j])
            )
        elif s[i] == s[j]:
            test = (
                s12[SA12[t] - n0 + 1] <= s12[j // 3 + n0]
                if (s[i + 1] == s[j + 1])
                else s[i + 1] < s[j + 1]
            )
        else:
            test = s[i] < s[j]

        if test:
            SA[k] = i
            t += 1
            if t == n02:
                k += 1
                l = n0 - p
                while p < n0:
                    SA[k] = SA0[p]
                    p += 1
                    k += 1

        else:
            SA[k] = j
            p += 1
            if p == n0:
                k += 1
                while t < n02:
                    SA[k] = (
                        (SA12[t] * 3) + 1 if SA12[t] < n0 else ((SA12[t] - n0) * 3) + 2
                    )
                    t += 1
                    k += 1
        k += 1


def radixpass(a, b, text, n, alpha):
    """The text is shifted by i = 2, 1, 0"""
    c = {}  # an array can be used
    for char in alpha:
        c[char] = 0

    for i in range(n):
        c[text[a[i]]] += 1

    s = 0  # sum
    for ch in alpha:
        freq, c[ch] = c[ch], s
        s += freq

    for i in range(n):
        b[c[text[a[i]]]] = a[i]
        c[text[a[i]]] += 1

    return b


def lcp_kasai(s, suffix_array):
    n = len(s)
    rank = array("i", [0 for _ in range(n + 1)])
    LCP = array("i", [0 for _ in range(n + 1)])
    for i in range(n):
        rank[suffix_array[i]] = i
    h = 0
    for j in range(n):
        h = max(0, h - 1)
        i = rank[j]
        j2 = suffix_array[i - 1]
        if i:
            while h + j < n and h + j2 < n and s[j + h] == s[j2 + h]:
                h += 1
            LCP[i - 1] = h
        else:
            h = 0
    return LCP


if __name__ == "__main__":
    t = "yabbadabbadoo"
    sa = construct_suffix_array(t)
    lcp = lcp_kasai(t, sa)
    print(sa, lcp)
