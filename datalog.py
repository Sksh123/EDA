from prettytable import PrettyTable

# Define the Assembly relation with rule types and quantities
assembly = [
    ("trike", "wheel", "contains", 3),
    ("trike", "seat", "contains", 1),
    ("trike", "pedal", "contains", 2),
    ("wheel", "rim", "component", 1),
    ("wheel", "tube", "component", 1),
    ("pedal", "spoke", "component", 10),
    ("seat", "cushion", "component", 1)
]

def components():
    components_dict = {}


    for part, subpart, rule_type, qty in assembly:
        if (part, subpart) not in components_dict:
            components_dict[(part, subpart)] = {'quantity': qty}
        else:
          
            if rule_type == 'contains':
                components_dict[(part, subpart)]['quantity'] += qty

    return components_dict


components_relation = components()


components_data = []
for component, info in components_relation.items():
    part, subpart = component
    quantity = info['quantity']
    components_data.append([part, subpart, quantity])


components_table = PrettyTable(['Part', 'Subpart', 'Quantity'])
for row in components_data:
    components_table.add_row(row)
print("Components Relation:")
print(components_table)


target_part = 'trike'
target_components_data = []
for component, info in components_relation.items():
    part, subpart = component
    if part == target_part:
        quantity = info['quantity']
        target_components_data.append([part, subpart, quantity])


target_components_table = PrettyTable(['Part', 'Subpart', 'Quantity'])
for row in target_components_data:
    target_components_table.add_row(row)
print(f"\nComponents of '{target_part}':")
print(target_components_table)
