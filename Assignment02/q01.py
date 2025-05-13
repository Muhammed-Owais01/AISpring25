def query(x):
    return -1 * (x - 7)**2 + 49

def find_peak(N: int) -> int:
    left, right = 0, N
    while left < right:
        mid = (left + right) // 2
        if query(mid) < query(mid + 1):
            left = mid + 1
        else:
            right = mid
    return left
