# Chemical Reaction Simulator
# Introduction
Chemical Reaction Simulator is a Python package designed to model and analyze chemical reaction dynamics. Utilizing a system of ordinary differential equations (ODEs), the package can simulate the time evolution of concentrations of various species in a reaction network. It can also visualize the reaction network graphically.

# Features
Define Complex Reactions: Users can define complex chemical reactions with reversible and irreversible reactions, involving multiple reactants and products.

1. **Fixed Concentrations:** Ability to set fixed concentrations for certain substances so that their concentrations do not change throughout the reaction.

2. **Reaction Network Visualization:** Graphical representation of the reaction network, showcasing the relations between reactants and products along with the reaction constants.

3. **Flexible Initial Concentrations:** Allows setting initial concentrations as a dictionary, providing flexibility in initializing the reaction setup.

4. **Data Visualization:** The package integrates with seaborn to facilitate plotting of concentration profiles over time.

# Installation
Clone the repository to your local machine:

git clone https://github.com/yourusername/chemical-reaction-simulator.git

# Usage
Here's a basic usage example:

from chemical_reaction_simulator import Reaction
import numpy as np
import seaborn as sns

# Define the reaction list
reaction_list = [
    ['Ni + C2 <-> NiC2', 1e-2, 1e-3],
    ['NiC2 + C2 -> NiC4', 1e-2]
]

# Create a Reaction object
reaction = Reaction(reaction_list, fixed_concentrations=['C2'])

# Solve the reaction system with initial concentrations
df = reaction.solve({'C2': 1, 'Ni': 1}, np.linspace(0, 10000, 1000))

# Plot the results
sns.lineplot(df[['C2']])


# Contributing
We welcome contributions to this project. Please feel free to open an issue or submit a pull request.

# License
----

# Contact
For any inquiries or discussions related to this project, please reach out to (your contact information).

Feel free to adjust any part of the README to better suit your project's specifics!