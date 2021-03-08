"""
Author: Edward Herrin
Date: 02/10/2020
Description: This program utilizes three timed runs of a hill climbing agent to determine a series of
    mathematical operations upon 100 random single digit numbers which approaches a given target value.
    Usage is as follows: "AI_Mathematical_Approximator.py <target_value>"
"""
# Required for discovering all possible number swaps.
import itertools
# Required for values calculations.
import math
# Required for discovering all possible operator changes.
import operator
# Required for making various random choices such as finding the random start state.
import random
# Required for processing command line arguments.
import sys
# Required for timing the three hill-climbing agent runs.
import time

"""
Description: This is the class for the hill-climbing agent and as such, will generate a hill-climbing agent
    with all the abilities that are required to perform rationally.
"""


class Agent(object):
    """
    Description: This is the initialization function for the hill-climbing agent and is responsible for setting up
        the current state and goal value knowledge for the agent.

    Returns: Nothing
    """
    def __init__(self, current_state, goal_value):
        # An array of the randomly generated set of single digit numbers
        self.goal_value = goal_value
        # The StateNode that represents the current state.
        self.current_state = current_state

    """
    Description: This function will determine the distance from the target value when it is given a node and then
        will store this distance value within the node.
        
    Returns: Nothing
    """

    def determine_distance_from_goal(self, current_state, goal_value):
        operations_set = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
        statement_array = []
        for character in current_state.statement:
            statement_array.append(character)
        element_index_start = 0
        first_digit = statement_array[element_index_start]
        element_index_start += 1
        operation = statement_array[element_index_start]
        element_index_start += 1
        second_digit = statement_array[element_index_start]
        element_index_start += 1
        result = operations_set[operation](int(first_digit), int(second_digit))
        for element_index in range(element_index_start, len(statement_array), 2):
            operation = statement_array[element_index]
            second_digit = statement_array[element_index + 1]
            result = operations_set[operation](result, int(second_digit))
        distance_from_goal = abs(goal_value - result)
        current_state.distance_from_goal = distance_from_goal

    """
    Description: This function will choose a successor node based upon the exact specifications that are
        provided in the class textbook for a hill-climbing agent.
        
    Returns: A StateNode.
    """

    def choose_successor_state(self, current_state):
        min_distance_from_goal = current_state.distance_from_goal
        candidate_nodes = []
        # Iterate through all of the current nodes children and determine the child with the smallest
        # Distance from the goal value
        for child in current_state.children:
            if child.distance_from_goal < min_distance_from_goal:
                candidate_nodes.append(child)
        # If there are no children with a smaller distance from the target
        if len(candidate_nodes) == 0:
            candidate_node = current_state
            return candidate_node
        # Otherwise, choose randomly from the list of children with smaller distances from the target
        else:
            candidate_node = candidate_nodes[random.randint(0, len(candidate_nodes) - 1)]
            return StateNode(candidate_node.statement, current_state, candidate_node.distance_from_goal)

    """
    Description: This function will ensure that a swap does not result in division
        by zero.
        
    Returns: Boolean.
    """

    def test_swap_validity(self, statement, goal_value):
        try:
            temp = StateNode(statement, "Null", math.inf)
            self.determine_distance_from_goal(temp, goal_value)
            return True
        except:
            return False

    """
    Description: This function will ensure that a sign change does not result in division
        by zero.
        
    Returns: Boolean.
    """

    def test_sign_change_validity(self, statement, goal_value):
        try:
            temp = StateNode(statement, "Null", math.inf)
            self.determine_distance_from_goal(temp, goal_value)
            return True
        except:
            return False

    """
    Description: This function will use the Agent's perform_swap function in such
        a way that all possible valid swaps will be added as child StateNodes for the 
        agent to analyse.
        
    Returns: Nothing.
    """

    def generate_local_swaps(self, current_state, goal_value):
        statement_array = []
        swapped_statements = []
        digit_indices = []
        for character in current_state.statement:
            statement_array.append(character)
        for character_index in range(0, len(statement_array), 2):
            digit_indices.append(character_index)
        all_local_swaps = list(itertools.combinations(digit_indices, 2))
        for swap in all_local_swaps:
            temp_statement_array = statement_array.copy()
            index1 = swap[0]
            index2 = swap[1]
            temp = temp_statement_array[index1]
            temp_statement_array[index1] = temp_statement_array[index2]
            temp_statement_array[index2] = temp
            if self.test_swap_validity(''.join(temp_statement_array), goal_value):
                swapped_statements.append(''.join(temp_statement_array))
        for statement in swapped_statements:
            temp_child = StateNode(statement, current_state, math.inf)
            self.determine_distance_from_goal(temp_child, goal_value)
            current_state.add_to_children(temp_child)

    """
    Description: This function will use the Agent's perform_sign_change function
        in such a way that all possible valid sign changes will be added as child 
        StateNodes for the agent to analyse.
        
    Returns: Nothings.
    """

    def generate_local_sign_changes(self, current_state, goal_value):
        statement_array = []
        altered_statement_array = []
        operations_set = ["+", "-", "*", "/"]
        for character in current_state.statement:
            statement_array.append(character)
        for element_index in range(0, len(statement_array)):
            temp_operations_set = operations_set.copy()
            if statement_array[element_index] in temp_operations_set:
                temp_statement_array = statement_array.copy()
                temp_operations_set.pop(temp_operations_set.index(statement_array[element_index]))
                for operation in temp_operations_set:
                    temp_statement_array[element_index] = operation
                    altered_statement = ''.join(temp_statement_array)
                    if self.test_sign_change_validity(altered_statement, goal_value):
                        altered_statement_array.append(altered_statement)
        for statement in altered_statement_array:
            temp_child = StateNode(statement, current_state, math.inf)
            self.determine_distance_from_goal(temp_child, goal_value)
            current_state.add_to_children(temp_child)

    """
    Description: This function will set the current state as the state that is given.
        
    Returns: Nothing.
    """

    def move_to_state(self, state):
        self.current_state = state


"""
Description: This function will generate a node which has a parent and children. Although a parent is not used for
    a hill-climbing agent, I kept it around for debugging purposes and possible future expansion.
        
Returns: Nothing.
"""


class StateNode(object):
    """
    Description: This is the initialization function for the StateNode. and will up all the necessary
        attributes.

    Returns: Nothing.
    """
    def __init__(self, statement, parent_node, distance_from_goal):
        # This is the parent node
        self.parent = parent_node
        # This is the state node's array of child nodes
        self.children = []
        # This is the statement that is evaluated
        self.statement = statement
        # This is the floating point value for the nodes distance from the goal value
        self.distance_from_goal = distance_from_goal

    """
    Description: This function will append a child node to the list of children for the node.
        
    Returns: Nothing.
    """
    def add_to_children(self, state):
        self.children.append(state)


"""
Description: This function will generate a random start statement from a provided set of 100 random
    single digits.
Returns: String.
"""


def generate_random_start_state(single_digit_set):
    random_start_state = ""
    operations_set = ["+", "-", "*", "/"]
    first_digit_choice = ""
    while len(single_digit_set) != 0:
        if first_digit_choice is "":
            first_digit_choice_index = random.randint(0, len(single_digit_set) - 1)
            first_digit_choice = str(single_digit_set[first_digit_choice_index])
            single_digit_set.pop(first_digit_choice_index)
        if len(single_digit_set) != 1:
            second_digit_choice_index = random.randint(0, len(single_digit_set) - 1)
            second_digit_choice = str(single_digit_set[second_digit_choice_index])
            single_digit_set.pop(second_digit_choice_index)
        else:
            second_digit_choice_index = 0
            second_digit_choice = str(single_digit_set[second_digit_choice_index])
            single_digit_set.pop(second_digit_choice_index)
        operation_choice_index = random.randint(0, len(operations_set) - 1)
        operation_choice = operations_set[operation_choice_index]
        while operation_choice is '/' and second_digit_choice == "0":
            operation_choice_index = random.randint(0, len(operations_set) - 1)
            operation_choice = operations_set[operation_choice_index]
        if len(single_digit_set) != 0:
            random_start_state += first_digit_choice + operation_choice
        else:
            random_start_state += first_digit_choice + operation_choice + second_digit_choice
        first_digit_choice = second_digit_choice
    return random_start_state


"""
Description: This function will generate a random set of single digit numbers.

Returns: A random set of single digit numbers
"""


def generate_set_of_single_digits():
    single_digit_set = []
    for single_digit in range(0, 100):
        single_digit_set.append(random.randint(0, 9))
    return single_digit_set


"""
Description: This is the main function that will call all of the necessary functions for generating the
    random state, creating the hill-climbing agent, and applying the hill-climbing agent to the random
    state for three timed runs.
Returns: Nothing.
"""


def main():
    goal_value = int(sys.argv[1])
    # This will set the stop time for each agent.
    number_set = generate_set_of_single_digits()
    number_set_copy = number_set.copy()
    # Run the program three times with three different durations.
    print("Number Set:", number_set_copy, "\n"
          + "Target:", goal_value, "\n")
    stop_time_set = []
    timer_start = time.time()
    time.process_time()
    # Runtime number one is for ten seconds.
    stop_time_set.append(5)
    # Runtime number two is for twenty seconds.
    stop_time_set.append(10)
    # Runtime number three is for thirty seconds.
    stop_time_set.append(15)
    iteration = 1
    overall_best = math.inf
    seconds_elapsed = 0
    for stop_time in stop_time_set:
        random_start_state = generate_random_start_state(number_set_copy)
        # This will create a StateNode object from a random start state and assign it to current_state.
        current_state = StateNode(random_start_state, "NULL", math.inf)
        # This will create an Agent object with basic initialization data.
        hill_climbing_agent = Agent(current_state, goal_value)
        # This will set the distance from the goal for the node provided.
        hill_climbing_agent.determine_distance_from_goal(current_state, hill_climbing_agent.goal_value)
        print("***************************************\nRR Iteration:", iteration, "\t\tt =", stop_time, "seconds")
        print("\tS0:", hill_climbing_agent.current_state.statement)
        if iteration == 1:
            print("\tDistance From Target", hill_climbing_agent.current_state.distance_from_goal)
        else:
            print("\tDistance From Target", hill_climbing_agent.current_state.distance_from_goal,
                  "\t\tOverall Best:", overall_best)
        while hill_climbing_agent.current_state.distance_from_goal != 0:
            if seconds_elapsed < stop_time:
                seconds_elapsed = math.floor(time.time() - timer_start)
                # This will generate all of the possible local swap options.
                hill_climbing_agent.generate_local_swaps(hill_climbing_agent.current_state, goal_value)
                # This will generate all of the possible local sign change options.
                hill_climbing_agent.generate_local_sign_changes(hill_climbing_agent.current_state, goal_value)
                successor_state = hill_climbing_agent.choose_successor_state(hill_climbing_agent.current_state)
                hill_climbing_agent.move_to_state(successor_state)
                print("\n\tBest State:", hill_climbing_agent.current_state.statement)
                print("\tDistance From Target", hill_climbing_agent.current_state.distance_from_goal)
                if hill_climbing_agent.current_state.distance_from_goal < overall_best:
                    overall_best = hill_climbing_agent.current_state.distance_from_goal
            else:
                break
        iteration += 1
        number_set = generate_set_of_single_digits()
        number_set_copy = number_set.copy()
        timer_start = time.time()
        seconds_elapsed = 0


if __name__ == '__main__':
    main()
