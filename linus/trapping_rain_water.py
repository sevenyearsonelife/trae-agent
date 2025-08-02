# 双指针法解决接雨水问题

def trap(height):
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    result = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                result += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                result += right_max - height[right]
            right -= 1
    
    return result

# 测试示例
height = [0,1,0,2,1,0,1,3,2,1,2,1]
print(trap(height))
