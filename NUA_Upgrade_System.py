# Will Koenig
# M4.B4 Module 4 Priority Queues and Heaps Application Programming Assignment

# Import UUID module to generate unique confirmation codes for all of our flyers
import uuid


class AVLTreeNode:
    def __init__(self, upgradeRequest):
        # Initialize a node with an upgrade request
        self.upgradeRequest = upgradeRequest
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        # Initialize an empty AVL tree
        self.root = None

    def insert(self, upgradeRequest):
        # Insert a new upgrade request into the AVL tree
        node = AVLTreeNode(upgradeRequest)
        if self.root is None:
            # If the tree is empty, set the new node as the root
            self.root = node
        else:
            # Otherwise, call the recursive helper method to insert the node
            self.root = self._insert_helper(self.root, node)

    def _insert_helper(self, root, node):
        # Recursive helper method to insert a node into the AVL tree
        if root is None:
            return node

        if node.upgradeRequest < root.upgradeRequest:
            # Insert the node in the left subtree
            root.left = self._insert_helper(root.left, node)
        else:
            # Insert the node in the right subtree
            root.right = self._insert_helper(root.right, node)

        # Update the height of the current node
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Check the balance factor and perform rotations if necessary
        balance = self._get_balance(root)

        if balance > 1 and node.upgradeRequest < root.left.upgradeRequest:
            return self._rotate_right(root)

        if balance < -1 and node.upgradeRequest > root.right.upgradeRequest:
            return self._rotate_left(root)

        if balance > 1 and node.upgradeRequest > root.left.upgradeRequest:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if balance < -1 and node.upgradeRequest < root.right.upgradeRequest:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def remove(self, upgradeRequest):
        # Remove a specific upgrade request from the AVL tree
        self.root = self._remove_helper(self.root, upgradeRequest)

    def _remove_helper(self, root, upgradeRequest):
        # Recursive helper method to remove a node from the AVL tree
        if root is None:
            return root

        if upgradeRequest == root.upgradeRequest:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            else:
                # Find the successor of the node and replace it with the current node
                successor = self._get_min_node(root.right)
                root.upgradeRequest = successor.upgradeRequest
                root.right = self._remove_helper(root.right, successor.upgradeRequest)

        elif upgradeRequest < root.upgradeRequest:
            root.left = self._remove_helper(root.left, upgradeRequest)
        else:
            root.right = self._remove_helper(root.right, upgradeRequest)

        # Update the height of the current node
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # Check the balance factor and perform rotations if necessary
        balance = self._get_balance(root)

        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._rotate_right(root)

        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._rotate_left(root)

        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def _get_height(self, node):
        # Get the height of a node
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        # Get the balance factor of a node
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        # Perform a left rotation around the given node
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        # Update the heights of the affected nodes
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, z):
        # Perform a right rotation around the given node
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        # Update the heights of the affected nodes
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_min_node(self, root):
        # Get the node with the minimum value in the given subtree
        current = root
        while current.left is not None:
            current = current.left
        return current

    def remove_highest_priority(self):
        # Remove and return the upgrade request with the highest priority
        if self.root is None:
            return None

        # Find the node with the highest priority i.e. the right-most node
        highest_priority = self._get_max_node(self.root)
        self.remove(highest_priority.upgradeRequest)

        return highest_priority.upgradeRequest

    def _get_max_node(self, current):
        # Get the node with the maximum value in the given subtree
        while current.right is not None:
            current = current.right
        return current

    def print_in_order(self):
        # Print the upgrade requests in order and return the list of upgrade requests
        return self._print_in_order_helper(self.root)

    def _print_in_order_helper(self, current):
        # Recursive helper method to traverse the tree in order
        result = []
        if current is not None:
            result.extend(self._print_in_order_helper(current.left))
            result.append(current.upgradeRequest)
            result.extend(self._print_in_order_helper(current.right))
        return result


class UpgradeRequest:
    def __init__(self, flyer_id, status):
        self.id = flyer_id
        self.status = status
        self.confirmation_code = uuid.uuid4().hex[:8]

    def __lt__(self, other):
        status_dict = {'silver': 1, 'gold': 2, 'platinum': 3, 'super': 4}
        return status_dict[self.status] <= status_dict[other.status]

    def __str__(self):
        return f"Flyer: {self.id}, Status: {self.status}, Confirmation Code: {self.confirmation_code}"

class WaitingList:
    def __init__(self):
        self.code_dictionary = {}
        self.AVL = AVLTree()

    def handleUpgradeRequest(self, upgradeRequest):
        # add to code dictionary { confirmation_code : upgradeRequest }
        self.code_dictionary[upgradeRequest.confirmation_code] = upgradeRequest

        # add to the binary search tree
        self.AVL.insert(upgradeRequest)


    def handleCancelUpgrade(self, confirmation_key):
        if confirmation_key not in self.code_dictionary:
            return None

        # find the upgrade request to be removed
        upgradeRequest = self.code_dictionary[confirmation_key]
        # remove from code dictionary
        del self.code_dictionary[confirmation_key]
        # remove from BST --> O(log n)
        self.AVL.remove(upgradeRequest)
        # remove from Priority Queue
        return upgradeRequest

    def print_ordered_waiting_list(self):
        waitList = self.AVL.print_in_order()
        waitList.reverse()
        return waitList



    def find_K_highest_priority(self, k):
        upgrades = []
        while k > 0:
            highest_priority = self.AVL.remove_highest_priority()
            if highest_priority:
                upgrades.append(highest_priority)
            else:
                break
            k -= 1
        return upgrades

if __name__ == '__main__':
    # create a new instance of the WaitingList class
    waitingList = WaitingList()

    while True:
        # Prompt the user for which operation they would like to complete
        print('Select an option: ')
        print('1. Request an upgrade')
        print('2. Cancel upgrade request')
        print('3. Get highest priority flyers')
        print('4. Print ordered wait list')
        print('5. Exit')
        choice = input("Enter your choice ")

        if choice == "1":
            # Prompt user for necessary info
            flyer_id = input("\nEnter the flyers id: ")

            correct_status = False
            while True:
                status = input("Enter the flyers status {silver, gold, platinum, or super}: ")
                if status in ['silver', 'gold', 'platinum', 'super']:
                    break
                else:
                    print('Incorrect status please try again')

            # Create a new Upgrade Request and add to the waitingList
            upgradeRequest = UpgradeRequest(flyer_id, status)
            waitingList.handleUpgradeRequest(upgradeRequest)

            # Print the upgrade request for the user's records
            print("Upgrade Request generated for:")
            print(upgradeRequest.__str__(), '\n')

        elif choice == "2":
            # Prompt the user for their 8 digit confirmation code and remove from waitingList
            user_confirmation_code = input("\nEnter the 8 digit confirmation code you received: ")

            upgradeRequest = waitingList.handleCancelUpgrade(user_confirmation_code)
            if upgradeRequest:
                print("Removing Upgrade Request for:")
                print(upgradeRequest.__str__(), '\n')
            else:
                print('No such upgrade request in our system \n')


        elif choice == "3":
            # Prompt the user for the number of available seats
            available_seats = int(input("\nHow many available upgrades are there: "))
            # Retrieve the K highest priority fliers from the waiting List
            upgrades = waitingList.find_K_highest_priority(available_seats)
            # confirm that our list is not empty
            if upgrades:
                for i in range(len(upgrades)):
                    current_upgrade = upgrades[i]
                    print(i + 1, current_upgrade.__str__())
                print("\n")
            else:
                print('There are no flyers on the waiting list\n')


        elif choice == "4":
            print("\nPrinting ordered waiting list")
            waitList = waitingList.print_ordered_waiting_list()
            if not waitList:
                print('No flyers are on the waitlist yes\n')
            else:
                for i in range(len(waitList)):
                    current = waitList[i]
                    print(i + 1, current.__str__())
                print('\n')


        elif choice == "5":
            print("Closing upgrade system and deleting stored upgrades, Goodbye")
            break

        else:
            print('Invalid choice, please try again. \n')
