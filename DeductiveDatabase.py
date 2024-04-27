class Assembly:
    def __init__(self, subpart, part, quantity):
        self.part = part
        self.subpart = subpart
        self.quantity = quantity

def remove_duplicates(assembly):
    unique_assembly = []
    for fact in assembly:
        is_duplicate = False
        for unique_fact in unique_assembly:
            if (fact.part == unique_fact.part and
                fact.subpart == unique_fact.subpart and
                fact.quantity == unique_fact.quantity):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_assembly.append(fact)
    return unique_assembly

def generate_all_subparts(component, assembly):
    print("\n---Parts and Subparts of", component, "---\n")
    print("Part Subpart Quantity")
    for fact in assembly:
        if fact.part == component:
            print(fact.part, fact.subpart, fact.quantity)

def apply_second_rule(assembly):
    new_facts = []
    for fact1 in assembly:
        for fact2 in assembly:
            if fact1.part == fact2.subpart:
                new_facts.append(Assembly(fact1.subpart, fact2.part, fact1.quantity))
    assembly.extend(new_facts)
    return assembly

def main():
    assembly = [
        Assembly("Wheel", "Trike", 3),
        Assembly("Frame", "Trike", 1),
        Assembly("Spoke", "Wheel", 2),
        Assembly("Tyre", "Wheel", 1),
        Assembly("Seat", "Frame", 1),
        Assembly("Pedal", "Frame", 1),
        Assembly("Tube", "Tyre", 1),
        Assembly("Rim", "Tyre", 1)
    ]

    print("---Applying first rule---\n")
    print("Part Subpart Quantity")
    for result in assembly:
        print(result.part, result.subpart, result.quantity)

    # Applying the second rule
    assembly = apply_second_rule(assembly)

    print("\n---Applying second rule---\n")
    print("Part Subpart Quantity")
    for fact in assembly:
        print(fact.part, fact.subpart, fact.quantity)

    # Applying the second rule twice
    assembly = apply_second_rule(assembly)
    assembly = remove_duplicates(assembly)

    component = input("\nEnter a component: ")
    generate_all_subparts(component, assembly)

if __name__ == "__main__":
    main()
