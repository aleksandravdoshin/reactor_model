import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import pandas as pd
import seaborn as sns

class Reaction:
    def __init__(self, reactions, fixed_concentrations=None) -> None:
        """
        Initialize the Reaction class with a list of reactions.
        
        Parameters:
        reactions (list): A list of reactions with associated rate constants.
        """
        self.reactions = reactions
        self.create_edges()
        self.G = nx.DiGraph()
        self.G.add_edges_from(self.edges)
        self.fixed_concentrations = fixed_concentrations or []

    def create_edges(self):
        """
        Creates edges representing the reactions between different substances. 
        It identifies the reactants and products and their respective rate constants for each reaction.
        """
        self.edges = []
        reaction_type_counter = 0

        for reaction in self.reactions:
            reaction_type_counter += 1
            reactants, products = reaction[0].split('<->') if '<->' in reaction[0] else reaction[0].split('->')
            rate_constants = reaction[1:]
            
            reactants = reactants.strip().split(' + ')
            products = products.strip().split(' + ')

            for reactant in reactants:
                for product in products:
                    self.edges.append((reactant.strip(), product.strip(), {'weight': rate_constants[0], 'type': f'k_{reaction_type_counter}'}))

            if '<->' in reaction[0] and len(rate_constants) > 1:
                reaction_type_counter += 1
                for reactant in reactants:
                    for product in products:
                        self.edges.append((product.strip(), reactant.strip(), {'weight': rate_constants[1], 'type': f'k_{reaction_type_counter}'}))


    def create_reaction_dict(self):
        """
        Creates a dictionary representing the reactions in the network.
        The dictionary groups substances based on the type of reactions they are involved in and calculates the rate constants for each grouped reaction.

        Returns:
        dict: A dictionary representing the grouped reactions and their rate constants.
        """
        self.reaction_dict = {}

        for node in self.G.nodes():
            in_edges = self.G.in_edges(node, data=True)
            out_edges = self.G.out_edges(node, data=True)

            type_groups = {}
            for u, v, data in in_edges:
                reaction_type = data['type']
                rate_constant = data['weight']

                if reaction_type not in type_groups:
                    type_groups[reaction_type] = {'nodes': set(), 'rate': rate_constant}
                type_groups[reaction_type]['nodes'].add(u)

            for u, v, data in out_edges:
                reaction_type = data['type']
                rate_constant = -data['weight']
                
                if reaction_type not in type_groups:
                    type_groups[reaction_type] = {'nodes': set(), 'rate': rate_constant}
                type_groups[reaction_type]['nodes'].add(node)

                neighbors_in_edges = self.G.in_edges(v, data=True)
                for nu, nv, ndata in neighbors_in_edges:
                    if ndata['type'] == reaction_type and nu != node:
                        type_groups[reaction_type]['nodes'].add(nu)
                
            self.reaction_dict[node] = [(tuple(group['nodes']), group['rate']) for group in type_groups.values()]

        return self.reaction_dict

    def rate_of_change(self, concs, t):
        """
        Calculate the rate of change of each substance at a given time point.

        Parameters:
        concs (list): List of current concentrations of the substances.
        t (float): Current time point.

        Returns:
        list: List of rate of changes of the substances.
        """
        conc_dict = {key: value for key, value in zip(self.sorted_keys, concs)}
        rate_dict = {key: 0 for key in self.sorted_keys}

        for substance, reactions_for_substance in self.reaction_dict.items():
            if substance in self.fixed_concentrations:
                rate_dict[substance] = 0
                continue

            for reaction in reactions_for_substance:
                rate = reaction[1]
                reactants = reaction[0]
                for reactant in reactants:
                    if reactant in conc_dict:
                        rate *= conc_dict[reactant]
                    else:
                        raise KeyError(f"Reactant {reactant} not found in the concentration dictionary")
                rate_dict[substance] += rate

        return [rate_dict[key] for key in self.sorted_keys]


    def solve(self, initial_concs_dict, time_points):
        # Getting sorted keys from the reaction dictionary
        if not hasattr(self, 'reaction_dict'):
            self.create_reaction_dict()
        if not hasattr(self, 'sorted_keys'):
            self.sorted_keys = sorted(self.reaction_dict.keys())

        # Preparing a list of initial concentrations in the same order as sorted keys
        initial_concs = [initial_concs_dict.get(key, 0) for key in self.sorted_keys]

        # Solving the differential equations
        solution = odeint(self.rate_of_change, initial_concs, time_points)

        # Creating a DataFrame from the solution
        df = pd.DataFrame(solution, columns=self.sorted_keys)
        df.index = time_points

        return df

        
    def plot_graph(self):
        """
        Plots a graphical representation of the reaction network using NetworkX and Matplotlib. 
        Displays the reactants, products, and the directions and rate constants of the reactions.
        """
        pos = nx.spring_layout(self.G)
        nx.draw_networkx(self.G, pos, with_labels=True, connectionstyle='arc3,rad=0.1', 
                         node_size=700, node_color='lightblue', font_size=10, font_color='black', 
                         edge_color='gray', width=2, alpha=0.6)

        # Display arrows indicating direction
        nx.draw_networkx_edge_labels(self.G, pos, 
                                     edge_labels={(u, v): f"{d['type']} ({d['weight']})" for u, v, d in self.G.edges(data=True)}, 
                                     label_pos=0.3)
        
        plt.show()