# ================================================================
# Problem: Construct Binary Tree from Inorder and Postorder Traversal
#
# Given two integer arrays representing inorder and postorder traversals
# of a binary tree, reconstruct and return the tree.
#
# Key Insights:
# • Postorder: [Left, Right, Root] → Last element is always root
# • Inorder: [Left, Root, Right] → Root splits left/right subtrees
# • Process postorder backwards while partitioning inorder array
#
# Time Complexity: O(n) where n = number of nodes
# Space Complexity: O(n) for hashmap + O(h) recursion stack
# ================================================================

from typing import List, Optional, Dict


class TreeNode:
    """Definition for a binary tree node."""
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        """
        Constructs a binary tree from inorder and postorder traversals.
        
        Args:
            inorder: List of node values in inorder sequence (Left-Root-Right)
            postorder: List of node values in postorder sequence (Left-Right-Root)
        
        Returns:
            Root node of the constructed binary tree, or None if empty
        
        Example:
            inorder = [9, 3, 15, 20, 7]
            postorder = [9, 15, 7, 20, 3]
            Output: [3, 9, 20, null, null, 15, 7]
        """
        if not inorder or not postorder:
            return None
        
        # Build value-to-index map for O(1) lookup in inorder array
        inorder_map: Dict[int, int] = {val: idx for idx, val in enumerate(inorder)}
        
        # Index pointer for postorder traversal (processed right-to-left)
        self.postorder_idx = len(postorder) - 1
        
        return self._build_tree_helper(
            postorder, 
            inorder_map, 
            left_bound=0, 
            right_bound=len(inorder) - 1
        )
    
    def _build_tree_helper(
        self, 
        postorder: List[int], 
        inorder_map: Dict[int, int],
        left_bound: int, 
        right_bound: int
    ) -> Optional[TreeNode]:
        """
        Recursively builds subtree within the given inorder bounds.
        
        Args:
            postorder: Complete postorder array
            inorder_map: HashMap of value → index in inorder array
            left_bound: Left boundary of current subtree in inorder
            right_bound: Right boundary of current subtree in inorder
        
        Returns:
            Root of the constructed subtree
        """
        # Base case: invalid range means no subtree exists
        if left_bound > right_bound:
            return None
        
        # Extract current root from end of postorder
        root_val = postorder[self.postorder_idx]
        self.postorder_idx -= 1
        
        # Create root node
        root = TreeNode(root_val)
        
        # Locate root position in inorder to partition left/right subtrees
        root_idx = inorder_map[root_val]
        
        # CRITICAL: Build RIGHT subtree BEFORE left
        # Since we're consuming postorder from right-to-left,
        # we encounter right subtree nodes before left subtree nodes
        root.right = self._build_tree_helper(
            postorder,
            inorder_map,
            root_idx + 1,  # Right subtree starts after root
            right_bound
        )
        
        root.left = self._build_tree_helper(
            postorder,
            inorder_map,
            left_bound,
            root_idx - 1   # Left subtree ends before root
        )
        
        return root


# ================================================================
# Alternative Approach: Iterative with Stack
# ================================================================

class SolutionIterative:
    """
    Iterative approach using explicit stack.
    More space-efficient in terms of call stack but harder to understand.
    """
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        if not inorder:
            return None
        
        stack = []
        root = TreeNode(postorder[-1])
        stack.append(root)
        inorder_idx = len(inorder) - 1
        
        # Process postorder from right to left (excluding last element)
        for i in range(len(postorder) - 2, -1, -1):
            node = TreeNode(postorder[i])
            parent = stack[-1]
            
            # Determine if node is right or left child
            if parent.val != inorder[inorder_idx]:
                parent.right = node
            else:
                # Backtrack to find correct parent for left child
                while stack and stack[-1].val == inorder[inorder_idx]:
                    parent = stack.pop()
                    inorder_idx -= 1
                parent.left = node
            
            stack.append(node)
        
        return root


# ================================================================
# Usage Example & Testing
# ================================================================

if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    inorder1 = [9, 3, 15, 20, 7]
    postorder1 = [9, 15, 7, 20, 3]
    tree1 = solution.buildTree(inorder1, postorder1)
    print("Tree 1 constructed successfully")
    
    # Test Case 2: Single node
    inorder2 = [1]
    postorder2 = [1]
    tree2 = solution.buildTree(inorder2, postorder2)
    print("Tree 2 constructed successfully")
    
    # Test Case 3: Empty tree
    tree3 = solution.buildTree([], [])
    print(f"Tree 3: {tree3}")  # Should be None