# Code From: https://github.com/lwcarani/matching-algorithms/
# For Proof of Concept and Testing Purposes

from typing import List, Set, Dict, Tuple, Iterable

from collections import defaultdict

from stable_matching import (
    generate_responses,
    generate_prefrence_list,
    flatten_preference_dictionary,
    ppdictionary,
    stable_matching_hetero,
    score_matching,
)


class Node(object):
    def __init__(self, name: str):
        self.name: str = name
        self.incoming_edges: Set[Tuple[str, str]] = set()
        self.outgoing_edges: Set[Tuple[str, str]] = set()

    def __repr__(self):
        return f"Node({self.name})"

    def get_next_node(self) -> str:
        return list(self.outgoing_edges)[0][1]

    def degree_outgoing(self) -> int:
        return len(self.outgoing_edges)

    def degree_incoming(self) -> int:
        return len(self.incoming_edges)


class Graph(object):
    def __init__(self, node_names: Iterable[str] = []):
        self.nodes: Dict[str, Node] = {name: Node(name) for name in node_names}
        self.edges: Set[Tuple[str, str]] = set()

    def __repr__(self):
        return (
            "Graph(\n  "
            + "\n  ".join(
                [f"{node}: {node.outgoing_edges}" for node in self.nodes.values()]
            )
            + "\n)"
        )

    def add_node(self, name: str):
        self.nodes[name] = Node(name)

    def delete_node(self, node: Node | str):
        if isinstance(node, Node):
            node: str = node.name

        connected_edges = (
            self.nodes[node].incoming_edges | self.nodes[node].outgoing_edges
        )
        for s, t in connected_edges:
            self.nodes[s].outgoing_edges.remove((s, t))
            self.nodes[t].incoming_edges.remove((s, t))
            self.edges.remove((s, t))

        del self.nodes[node]

    def number_of_nodes_in_graph(self) -> int:
        return len(self.nodes)

    def get_random_node(self) -> Node:
        for _, node in self.nodes.items():
            return node

    def add_edge(self, s: str, t: str):
        if s not in self.nodes.keys():
            self.add_node(s)
        if t not in self.nodes.keys():
            self.add_node(t)

        self.nodes[s].outgoing_edges.add((s, t))
        self.nodes[t].incoming_edges.add((s, t))
        self.edges.add((s, t))


def find_cycle(G: Graph) -> List[str] | None:
    if G.number_of_nodes_in_graph == 0:
        return None
    visited_nodes: Set[str] = set()
    cycle: List[str] = list()
    # start at an arbitrary node in the graph to begin random walk
    # repeat until we find a cycle. NOTE: a cycle is guaranteed to exist.
    n: Node = G.get_random_node()
    while n.name not in visited_nodes:
        visited_nodes.add(n.name)
        cycle.append(n.name)
        n: Node = G.nodes[n.get_next_node()]

    start_of_cycle_index = cycle.index(n.name)
    return cycle[start_of_cycle_index:]


def update_graph(
    G, matches, employee_preferences, job_preferences, employee_queue, job_queue
):
    employees = set(employee_preferences.keys())
    jobs = set(job_preferences.keys())

    for e in employees:
        # if the job that this employee was "pointing" at is no longer available,
        # add an edge between this employee and their next highest job preference
        if e in G.nodes.keys() and G.nodes.get(e).degree_outgoing() == 0:
            # increment counter so that next time through loop, we consider the next job on the preference list
            while True:
                job_queue[e] += 1
                job_index = job_queue[e]
                # add a directed edge from this employee to their next highest preference that is still available
                if job_index < len(employee_preferences[e]):
                    next_job_preference: str = employee_preferences[e][job_index]
                # if we've gone through the employee's entire list, assign employee to themself to indicate unmatched
                # delete them from the graph
                else:
                    matches[e] = e
                    G.delete_node(e)
                    break

                # if this employee's next highest preference has not yet been assigned, add a directed edge
                if next_job_preference not in matches:
                    G.add_edge(e, next_job_preference)
                    break

    for j in jobs:
        # if the employee that this job was "pointing" at is no longer available,
        # add an edge between this job and their next highest employee preference
        if j in G.nodes.keys() and G.nodes.get(j).degree_outgoing() == 0:
            # increment counter so that next time through loop, we consider the next employee on the preference list
            while True:
                employee_queue[j] += 1
                employee_index = employee_queue[j]
                # add a directed edge from this job to their next highest preference that is still available
                if employee_index < len(job_preferences[j]):
                    next_employee_preference: str = job_preferences[j][employee_index]
                # if we've gone through the job's entire list, this job will be unfilled,
                # delete it from the graph
                else:
                    G.delete_node(j)
                    break
                # if this job's next highest preference has not yet been assigned, add a directed edge
                if next_employee_preference not in matches:
                    G.add_edge(j, next_employee_preference)
                    break
    return G, matches, employee_queue, job_queue


def ttc(
    employee_preferences: Dict[str, List[str]], job_preferences: Dict[str, List[str]]
) -> Tuple[Dict[str, str], Dict[str, str]]:
    matches: Dict[str, str] = {}
    employees = set(employee_preferences.keys())
    jobs = set(job_preferences.keys())
    all_nodes = employees | jobs

    # instantiate a new Graph object with all employee and job nodes
    # initially, this graph will only have nodes, no edges
    G = Graph(all_nodes)

    # queue (counter) to track which job we are currently considering for the current employee
    # i.e., if job_index is 2, then we are considering the 3rd job on the given
    job_queue: Dict = defaultdict(int)
    employee_queue: Dict = defaultdict(int)

    # add edges to build out graph
    for e in employees:
        job_index = job_queue[e]  # new entries start at 0 for defaultdict
        G.add_edge(e, employee_preferences[e][job_index])
    for j in jobs:
        employee_index = employee_queue[j]  # new entries start at 0 for defaultdict
        G.add_edge(j, job_preferences[j][employee_index])

    # Remove top trading cycles until graph is empty
    while G.number_of_nodes_in_graph() > 0:
        # find an arbitrary cycle in the graph
        cycle = find_cycle(G)

        # make assignments of employees to job based on cycle that was found
        for node in cycle:
            if node in employees:
                job: str = G.nodes[node].get_next_node()
                matches[node] = job
                matches[job] = node
                G.delete_node(node)
                G.delete_node(job)

        # update the graph with new edges after cycle was found and matches were made
        G, matches, employee_queue, job_queue = update_graph(
            G, matches, employee_preferences, job_preferences, employee_queue, job_queue
        )

    return matches, {employee: matches[employee] for employee in employees}


if __name__ == "__main__":
    male = generate_responses()
    female = generate_responses()

    mpl, fpl = generate_prefrence_list(male, female)
    mpl, fpl = flatten_preference_dictionary(mpl, fpl)

    mpl = {str(i) + "M": [str(j) + "F" for j in mpl[i]] for i in mpl.keys()}
    fpl = {str(i) + "F": [str(j) + "M" for j in fpl[i]] for i in fpl.keys()}

    print("Preference Lists:")
    ppdictionary(mpl)

    ppdictionary(fpl)

    print("\nTop Trading Cycle:")

    _, matches = ttc(mpl, fpl)

    ppdictionary(matches)

    print(f"Score: {score_matching(matches, mpl, fpl)}")

    print("\nGale-Shapley:")

    matches = stable_matching_hetero(mpl, fpl)

    ppdictionary(matches)

    print(f"Score: {score_matching(matches, mpl, fpl)}")

    print("\nGale-Shapley Woman Optimal:")

    matches = stable_matching_hetero(fpl, mpl)

    ppdictionary(matches)

    print(f"Score: {score_matching(matches, fpl, mpl)}")
