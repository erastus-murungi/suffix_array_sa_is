# SA-IS
## A simple implementation of SA-IS.


### SA-IS(T):
 - Scan **T** from right-to-left to mark each character as **S-type** or **L-type**.
    Identify all the **LMS suffixes** of T.
 
 - Run induced sorting using the LMS suffixes in the order they appear in in T.
    Scan the result, gathering LMS suffixes in the order they ended up in.
 
 - Number the LMS blocks, assigning duplicate blocks the same number.
 
 - Form the reduced string **T’** from the block numbers.
 
 - If all blocks are unique, get a suffix array for T’ by directly inverting T’.
   Otherwise, get a suffix array for T’ by calling SA-IS(T’).
 
 - Use the suffix array for T’ to sort the LMS suffixes of T.
 - Do a second induced sorting pass of T using the LMS suffixes in sorted order.
 
## References:
[Linear Suffix Array Construction by Almost Pure
Induced-Sorting](https://ieeexplore.ieee.org/document/4976463)
