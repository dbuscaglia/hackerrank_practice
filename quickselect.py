"""
Select(A,n,i):
    Divide input into ⌈n/5⌉ groups of size 5.

    /* Partition on median-of-medians */
    medians = array of each group’s median.
    pivot = Select(medians, ⌈n/5⌉, ⌈n/10⌉)
    Left Array L and Right Array G = partition(A, pivot)

    /* Find ith element in L, pivot, or G */
    k = |L| + 1
    If i = k, return pivot
    If i < k, return Select(L, k-1, i)
    If i > k, return Select(G, n-k, i-k)
"""