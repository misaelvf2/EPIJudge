from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from collections import namedtuple

Result = namedtuple("Result", ["height", "balanced"])


def is_balanced_binary_tree(tree: BinaryTreeNode) -> bool:
    # Simple recursive solution based on postorder traversal.
    # Essentially the same algorithm used to compute the height of a binary tree,
    # but with extra logic to determien if tree is balanced.
    # Notice how we check whether the left subtree is balanced
    # so we don't waste time making recursive calls to the right subtree
    # if the left subtree is known to be unbalanced.
    # Time: O(n)
    # Space: O(h), reducing to O(n) for unbalanced/skewed binary trees,
    # and O(log n) for balanced binary trees.
    # Could squeeze out some additional efficiency if we used an iterative approach,
    # thought the space complexity would still be O(h).
    def is_height_balanced(node: BinaryTreeNode) -> Result:
        if not node:
            return Result(height=-1, balanced=True)
        left = is_height_balanced(node.left)
        if not left.balanced:
            return left
        right = is_height_balanced(node.right)
        if not right.balanced:
            return right
        balanced = abs(left.height - right.height) <= 1
        result = Result(
            height=max(left.height, right.height) + 1,
            balanced=balanced,
        )
        return result

    return is_height_balanced(tree).balanced


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_tree_balanced.py", "is_tree_balanced.tsv", is_balanced_binary_tree
        )
    )
