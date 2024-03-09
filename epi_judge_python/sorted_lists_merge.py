from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def merge_two_sorted_lists(
    L1: Optional[ListNode], L2: Optional[ListNode]
) -> Optional[ListNode]:
    # Very similar to my solution below, but much more elegant.
    # Creates a dummy head node to simplify the initialization logic.
    # Uses the term 'tail' to refer to the node that holds the current last
    # node in the merged list.
    # Uses L1 and L2 as pointers to iterate through the lists.
    # Exploits the linked list structure to add rest of
    # nodes after either L1 or L2 has run out, rather than iterating
    # through each remaining node one by one.
    # Also uses a simple boolean trick to simplify the logic.
    # Apart from that, many of the same considerations as before still apply.
    # Time: O(n + m)
    # Space: O(1)
    dummy_head = tail = ListNode()

    while L1 and L2:
        if L1.data <= L2.data:
            tail.next, L1 = L1, L1.next
        else:
            tail.next, L2 = L2, L2.next
        tail = tail.next

    tail.next = L1 or L2
    return dummy_head.next


def merge_two_sorted_lists_my_solution(
    L1: Optional[ListNode], L2: Optional[ListNode]
) -> Optional[ListNode]:
    # The tricky part, as for most linked list problems,
    # is pointer management. Notice how we need to keep
    # 4 separate pointers:
    # i and j to iterate through L1 and L2, respectively
    # result to keep track of the merged list's head node
    # and current to keep track of the current last node in the
    # merged list as we go.
    # The order in which we update the next pointer is *very*
    # important and easy to get wrong. Updating the next pointer
    # prior to advancing the iterator gives you an infinite loop!
    # Lastly, mind the edge case of an empty L1 or L2.
    # Time: O(n + m)
    # Space: O(1)
    if L1 is None:
        return L2
    if L2 is None:
        return L1

    result = min(L1, L2, key=lambda x: x.data)
    current = result

    i, j = L1, L2
    while i is not None and j is not None:
        if i.data <= j.data:
            i, current.next = i.next, i
        else:
            j, current.next = j.next, j
        current = current.next

    while i is not None:
        current.next = i
        i = i.next
        current = current.next

    while j is not None:
        current.next = j
        j = j.next
        current = current.next

    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sorted_lists_merge.py", "sorted_lists_merge.tsv", merge_two_sorted_lists
        )
    )
