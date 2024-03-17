from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


from collections import namedtuple, deque
import math


Result = namedtuple("Result", ["is_bst", "minimum", "maximum"])
BFSNode = namedtuple("BFSNode", ["node", "low", "high"])


def is_binary_tree_bst(tree: BinaryTreeNode) -> bool:
    # Same as below, but performs the inorder traversal
    # iteratively.
    stack = []
    current = tree
    last = -math.inf

    while current or stack:
        # Go as far to the left as possible
        while current:
            stack.append(current)
            current = current.left
        # Reached end of branch
        current = stack.pop()
        # Check whether current node satisfies BST condition
        if current.data < last:
            return False
        last = current.data
        # Now go right
        current = current.right

    return True


def is_binary_tree_bst_inorder_sort(tree: BinaryTreeNode) -> bool:
    # Perform an inorder traversal on the binary tree.
    # By definition, an inorder traversal on a BST
    # should yield all nodes in the BST in sorted order.
    # Accumulate the elements in a list. If at any point
    # there is an out-or-order element, return False.
    # Time: O(n)
    # Space: O(n)
    def inorder_dfs(node: BinaryTreeNode, elems: list[int]) -> bool:
        # Base condition: reached end of branch
        if node is None:
            return True
        left = inorder_dfs(node.left, elems)
        if not left:
            return False
        # Check that BST condition holds
        if len(elems) > 0 and node.data < elems[-1]:
            return False
        elems.append(node.data)
        right = inorder_dfs(node.right, elems)
        if not right:
            return False
        return True

    return inorder_dfs(tree, [])


def is_binary_tree_bst_bfs(tree: BinaryTreeNode) -> bool:
    # Same approach as top-down constraint propagation, but use
    # breadth-first search. Terminates early when violating nodes
    # are close to the root (i.e., at short depths). Trade-off
    # is increased space utilization!
    # Time: O(n)
    # Space: O(n)
    queue = deque([BFSNode(node=tree, low=-math.inf, high=math.inf)])

    while queue:
        node = queue.popleft()
        if node.node:
            if not node.low <= node.node.data <= node.high:
                return False
            if node.node.left:
                queue.append(
                    BFSNode(node=node.node.left, low=node.low, high=node.node.data)
                )
            if node.node.right:
                queue.append(
                    BFSNode(node=node.node.right, low=node.node.data, high=node.high)
                )

    return True


def is_binary_tree_bst_epi(tree: BinaryTreeNode) -> bool:  #
    # Same idea as my solution, but propagate the constraints from top to bottom.
    # Makes for much cleaner solution.
    # Time: O(n)
    # Space: O(h)
    def preorder_dfs(node: BinaryTreeNode, low: int, high: int) -> bool:
        if not node:
            return True
        if not low <= node.data <= high:
            return False
        # Could also do an early termination here.
        return preorder_dfs(node.left, low=low, high=node.data) and preorder_dfs(
            node.right, low=node.data, high=high
        )

    return preorder_dfs(tree, low=-math.inf, high=math.inf)


def is_binary_tree_bst_early_terminate(tree: BinaryTreeNode) -> bool:
    # Same solution as below, but with a small optimization: we terminate early by
    # we testing whether the left and right subtrees are themselves BSTs before continuing
    # down the call stack.
    # Time: O(n), since we must look at all nodes.
    # Space: O(h), where h = height of the binary tree.
    def postorder_dfs(node: BinaryTreeNode) -> Result:
        # Base case
        if node is None:
            return Result(is_bst=True, minimum=math.inf, maximum=-math.inf)
        left = postorder_dfs(node.left)
        if not left.is_bst:
            return Result(is_bst=False, minimum=None, maximum=None)
        right = postorder_dfs(node.right)
        if not right.is_bst:
            return Result(is_bst=False, minimum=None, maximum=None)
        if not (left.maximum <= node.data <= right.minimum):
            return Result(
                is_bst=False,
                minimum=min(node.data, left.minimum, right.minimum),
                maximum=max(node.data, left.maximum, right.maximum),
            )
        return Result(
            is_bst=True,
            minimum=min(node.data, left.minimum, right.minimum),
            maximum=max(node.data, left.maximum, right.maximum),
        )

    return postorder_dfs(tree).is_bst


def _is_binary_tree_bst(tree: BinaryTreeNode) -> bool:
    # Use post-order traversal to verify that BST condition holds
    # for all nodes.
    # The BST condition states that a node must be greater than or equal to
    # all nodes in its left subtree, and less than or equal to all nodes
    # in its right subtree.
    # It's very easy to make the mistake of only testing for the local condition
    # (that is, that root.left.data <= root.data <= root.right.data),
    # which does NOT imply that the BST condition holds globally.
    # To test for the global condition, we must keep track of the minimum and
    # maximum at the trees rooted in every node.
    # A node satisfies the BST condition if it is greater than or equal to
    # the maximum value in its left subtree, and less than or equal to
    # the minimum value in its right subtree.
    # We propagate the minimum and maximum up the call stack.
    # In other words, bottom-up constraint propagation.
    # This approach is more complicated because we're searching for minimum
    # and maximum in parallel with verifying whether the tree satisfies
    # the BST condition.
    # Time: O(n), since we must look at all nodes.
    # Space: O(h), where h = height of the binary tree.
    def postorder_dfs(node: BinaryTreeNode) -> Result:
        # Base case
        if node is None:
            return Result(is_bst=True, minimum=math.inf, maximum=-math.inf)
        left = postorder_dfs(node.left)
        right = postorder_dfs(node.right)
        # Very easy to get this mixed up!!!
        # Post-order is necessary because we need to know the minimum and maximum values
        # in the right and left subtrees, respectively.
        if not (left.maximum <= node.data <= right.minimum):
            return Result(
                is_bst=False,
                minimum=min(node.data, left.minimum, right.minimum),
                maximum=max(node.data, left.maximum, right.maximum),
            )
        return Result(
            is_bst=left.is_bst and right.is_bst,
            minimum=min(node.data, left.minimum, right.minimum),
            maximum=max(node.data, left.maximum, right.maximum),
        )

    return postorder_dfs(tree).is_bst


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_tree_a_bst.py", "is_tree_a_bst.tsv", is_binary_tree_bst
        )
    )
