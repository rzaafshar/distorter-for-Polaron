from pymatgen.core import Structure
import numpy as np

def find_first_neighbors(structure, atom_idx, search_radius=4.0, tol=0.8):
    center = structure[atom_idx]
    neighbors = structure.get_neighbors(center, search_radius)
    by_element = {}
    for n in neighbors:
        el = n.specie.symbol
        by_element.setdefault(el, []).append(n)
    first_shell = {}
    for el, ns in by_element.items():
        ns.sort(key=lambda n: n.nn_distance)
        d_min = ns[0].nn_distance
        first_shell[el] = [n for n in ns if n.nn_distance <= d_min * (1 + tol)]
    return first_shell

'''
def find_first_neighbors(structure, atom_idx, search_radius=4.0, tol=0.15, debug=True):
    center = structure[atom_idx]
    neighbors = structure.get_neighbors(center, search_radius)
    by_element = {}
    for n in neighbors:
        el = n.specie.symbol
        by_element.setdefault(el, []).append(n)

    first_shell = {}
    for el, ns in by_element.items():
        ns.sort(key=lambda n: n.nn_distance)
        if debug:
            print(f"  [debug] all {el} distances within {search_radius} Å: "
                  f"{[round(n.nn_distance, 3) for n in ns]}")
        d_min = ns[0].nn_distance
        first_shell[el] = [n for n in ns if n.nn_distance <= d_min * (1 + tol)]
    return first_shell

def find_first_neighbors(structure, atom_idx, search_radius=4.0, gap_ratio=1.3, debug=True):
    center = structure[atom_idx]
    neighbors = structure.get_neighbors(center, search_radius)
    by_element = {}
    for n in neighbors:
        el = n.specie.symbol
        by_element.setdefault(el, []).append(n)

    first_shell = {}
    for el, ns in by_element.items():
        ns.sort(key=lambda n: n.nn_distance)
        dists = [n.nn_distance for n in ns]
        if debug:
            print(f"  [debug] all {el} distances: {[round(d,3) for d in dists]}")

        # پیدا کردن اولین جهش بزرگ در فاصله‌ها
        cut = len(ns)
        for i in range(1, len(dists)):
            if dists[i] > dists[i-1] * gap_ratio:
                cut = i
                break
        first_shell[el] = ns[:cut]
    return first_shell
'''

def ask_percentage(el, count, dists):
    while True:
        raw = input(
            f"\nElement {el}: {count} neighbor(s), d = {dists}\n"
            f"Enter displacement percentage for {el} "
            f"(-100 to 100, negative = closer, positive = farther): "
        )
        try:
            val = float(raw)
        except ValueError:
            print("Invalid number, try again.")
            continue
        if -100 <= val <= 100:
            return val / 100.0
        print("Value must be between -100 and 100.")


def apply_distortion(structure, atom_idx, search_radius=4.0, tol=0.15):
    structure = structure.copy()
    center = structure[atom_idx]
    first_shell = find_first_neighbors(structure, atom_idx, search_radius, tol)

    print(f"\nCentral atom: {center.specie} (index {atom_idx + 1})")

    for el, ns in first_shell.items():
        dists = [round(n.nn_distance, 3) for n in ns]
        factor = ask_percentage(el, len(ns), dists)
        for n in ns:
            vec = n.coords - center.coords
            unit = vec / np.linalg.norm(vec)
            shift = unit * n.nn_distance * factor
            structure.translate_sites([n.index], shift,
                                      frac_coords=False, to_unit_cell=True)
    return structure


if __name__ == "__main__":
    struct = Structure.from_file("POSCAR")

    print("Atoms in POSCAR:")
    for i, site in enumerate(struct):
        print(f"  {i+1}: {site.specie} at {site.frac_coords.round(4)}")

    atom_number_1based = int(input("\nEnter atom number (1-based) to distort around: "))
    atom_idx = atom_number_1based - 1

    new_struct = apply_distortion(struct, atom_idx)
    new_struct.to(filename="POSCAR_distorted")
    print("\nSaved: POSCAR_distorted")
