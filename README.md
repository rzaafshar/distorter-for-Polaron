# distorter-for-Polaron
# distorter.py

A small interactive Python tool built on top of [pymatgen](https://pymatgen.org/) 
for generating **structurally distorted crystal structures**, primarily intended 
for polaron (localized defect) studies in DFT calculations.

## What it does

Given a `POSCAR` file, the script lets you:

1. **Pick a central atom** by its 1-based index from the structure.
2. **Automatically detect neighboring atoms** around that center within a fixed 
   search radius (default: 5 Å), grouped by chemical element.
3. **Interactively set a displacement percentage** (from -100% to +100%) 
   separately for each neighboring element/shell.
   - Positive values move the neighbor atoms **away** from the center.
   - Negative values move the neighbor atoms **closer** to the center.
4. **Apply the distortion** and write the modified structure to `POSCAR_distorted`.

This is useful for creating trial structures with a locally distorted 
coordination environment around a defect/dopant site — a common first step 
when searching for small-polaron configurations.

## Neighbor detection

Neighbors are found using a simple, fixed-radius search (`structure.get_neighbors`) 
rather than tolerance- or gap-ratio-based shell detection. This choice was made 
deliberately for defect-containing structures, where standard "first coordination 
shell" heuristics (distance tolerance, gap-ratio cutoffs) can misclassify 
neighbors due to local lattice relaxation around the defect. A fixed cutoff 
radius (default 5 Å) gives predictable, reproducible results regardless of 
how distorted the local environment already is.

## Usage
```bash
python distorter.py

The script will:
1. Print all atoms in `POSCAR` with their index, element, and fractional coordinates.
2. Ask you to select the central atom by index.
3. List all neighboring elements found within the search radius, along with 
   their distances from the center.
4. Prompt you for a displacement percentage for each element found.
5. Write the resulting structure to `POSCAR_distorted`.

## Requirements

- Python 3.x
- [pymatgen](https://pymatgen.org/)

## Notes

- Displacement percentages are relative to the original bond vector length 
  (center → neighbor).
- Different elements/shells can be distorted independently and in opposite 
  directions (e.g., anions pushed out while cations pulled in).


اگر بخواهید می‌توانم این را کوتاه‌تر (فقط چند خط برای بالای فایل به‌عنوان docstring/comment) هم بنویسم، یا این را مستقیماً به‌عنوان `README.md` در همان مسیر ذخیره کنم. کدام را ترجیح می‌دهید؟
