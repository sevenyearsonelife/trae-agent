class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root):
    if root is None:
        return None
    # 交换左右子树
    root.left, root.right = root.right, root.left
    # 递归翻转左子树
    invertTree(root.left)
    # 递归翻转右子树
    invertTree(root.right)
    return root