def trap(height):
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0
    while lo <= hi:
        if left_max <= right_max:
            left_max = max(left_max, height[lo])
            water += left_max - height[lo]
            lo += 1
        else:
            right_max = max(right_max, height[hi])
            water += right_max - height[hi]
            hi -= 1
    return water

assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
assert trap([4,2,0,3,2,5])             == 9
assert trap([])                         == 0
assert trap([5])                        == 0
assert trap([3,3])                      == 0
assert trap([2,0,2])                    == 2
print("all tests passed")
