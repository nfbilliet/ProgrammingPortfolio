import numpy as np 
import scipy.spatial as spatial
from h5py import File as f 
import os
import matplotlib.pyplot as plt
import math
#import torch
#import torch_geometric
from openbabel import pybel

#data_dir= "/home/nbilliet/projects/def-stijn/nbilliet/gqcg_data/QM9/data"
#test_file="dsgdb9nsd_108493.xyz"

test_smiles = ["COCC(=NC1C(O1)C)CCC(N)C(N(C))CC=O",
               "CC(OO)CN=NCC(F)CC(=O)F",
               "CC(=O)CC(=O)OC(=O)CC(=O)O"]

class ChemIdentifier():
    def __init__(self):
        self.smiles = None
        self.molecule = None
        self.atoms = None
        self.indices = None
        self.functional_groups = None
        self.hybridization = []

    def read_xyz(self, data_dir, filename):
        filepath=os.path.join(data_dir, filename)
        self.molecule=next(pybel.readfile("xyz", filepath))
        self.smiles = mol.write(format="smi")
        self.smiles = self.smiles.split()[0].strip()
        self.atoms = [atom.atomicnum for atom in self.molecule.atoms]
        self.indices = [atom.atomicnum for atom in self.molecule.atoms]
        self.hybridization = [atom.hyb for atom in self.molecule.atoms]

    def identify_funcgroup(self, molecule):
        """
        A function designed to identify the different functional groups in a molecule.
        To achieve this we provide a list of substructures that corresponds to different functional groups

            [Alkane, Alkene, Alkyn, Aromatic
            - Oxygen groups
                - Alcohol
                - Aldehyde
                - Keton
                - Ether
                - Peroxide
                - Epoxide
                - Carboxylic acid
                - Ester
                - Anhydride
                - Amide
                - Acyl halide
            - Nitrogen groups
                - Amine
                - Amide
                - Imine
                - Imide
                - Azide
                - Azo
                - Cyanates
                - Nitrate
                - Nitrile
                - Nitrite
                - Nitro
                - Nitroso
                - Oxime
            - Halogen groups
                -Halo alkane
        """
        #
        smarts_codes = ["[CX4]", "[#6]=[#6]", "[#6]#[#6]", "[c]",
                        "[#6][OX2H]", "[CX3H1](=O)", "[#6][CX3](=O)[#6]",
                        "[#6]O[#6]", "[#6]OO", "[#6]@O@[#6]", "[#6](=O)O", 
                        "[#6](=O)O[#6]", "[CX3](=[OX1])[OX2][CX3](=[OX1])",
                        "[NX3][CX3](=[OX1])[#6]","[#6][NX2]", 
                        "[$([CX3]([#6])[#6]),$([CX3H][#6])]=[$([NX2][#6]),$([NX2H])]",
                        "[$(*-[NX2-]-[NX2+]#[NX1]),$(*-[NX2]=[NX2+]=[NX1-])]", 
                        "[NX2]=[NX2]", "[OX2][CX2]#[NX1]", "[$([NX3](=[OX1])(=[OX1])O),$([NX3+]([OX1-])(=[OX1])O)]", 
                        "[NX1]#[CX2]", "[#6]ON=O", "[$([NX3](=O)=O),$([NX3+](=O)[O-])][!#8]", 
                        "[NX2]=[OX1]", "[#6][F,Cl,Br,I]"]
        smarts = [pybel.Smarts(smarts_code) for smarts_code in smarts_codes]
        nmb_atoms = len([atom for atom in molecule.atoms])
        functional_groups = [[]*nmb_atoms)]
        for class_idx, smart in enumerate(smarts):    
            indices=smart.findall(molecule)
            if indices!=[]:
                for idx in indices:
                    functional_groups[idx-1].append(class_idx+1)
        return functional_groups

def convert_str_to_float(str):
    if "*^" in str:
        return float(str.replace("*^", "e"))
    else:
        return float(str)

def format_xyz(root_dir,filename, atom_dict=dict(zip(["H", "C", "N", "O", "F"], [1,6,7,8,9]))):
    """
    A function that will process the xyz file which can be split up in the following way according 
    to each line

        1) Number of atoms (n)
        2) Scalar properties
            1 tag — ‘gdb9’string to facilitate extraction
            2) i — Consecutive, 1-based integer identifier
            3) A (GHz) - Rotational constant
            4) B (GHz) - Rotational constant
            5) C (GHz) - Rotational constant
            6) μ (D) - Dipole moment
            7) α (a^3_0) - Isotropic polarizability
            8) ε_{HOMO} (Ha) - Energy of HOMO
            9) ε_{LUMO} (Ha) - Energy of LUMO
            10) ε_{gap} (Ha) - Gap (ε_{LUMO}−ε_{HOMO})
            11) <R^2> (a^2_0) - Electronic spatial extent
            12) zpve (Ha) - Zero point vibrational energy
            13) U_0 (Ha) - Internal energy at 0 K
            14) U (Ha) - Internal energy at 298.15 K
            15) H (Ha) - Enthalpy at 298.15 K
            16) G (Ha) - Free energy at 298.15 K
            17) C_v (cal/mol.K) - Heat capacity at 298.15 K
        3-3+n) Molecular geometry
            1) Atom string
            2) x coordinate
            3) y coordinate
            4) z coordinate
            5) Mulliken charge (e)
        3+n+1) Harmonic vibrational frequencies
        3+n+2) SMILES string
            1) GDB-17
            2) B3LYP
        3+n+3) InChI strings
            1) Corina geometry
            2) B3LYP 

    Arguments
        :data_dir (str): The directory where the xyz file is stored
        :filename (str): The filename of the xyz file
    Returns
        ::
    """
    raw_dir = os.path.join(root_dir, "raw")
    filepath = os.path.join(raw_dir, filename)
    xyz_file = open(filepath, "r")
    lines = [line[:-1].split("\t") for line in xyz_file]
    scalar_properties = dict(zip(["A", "B", "C", "mu", "alpha", "E_h", "E_l", "E_g", "R_sq", "zpve", "U_0", "U", "H", "G", "C_v"],
                                [convert_str_to_float(el) for el in lines[1][1:-1]]))
    
    atoms = np.array([atom_dict[line[0]] for line in lines[2:-3]])
    positions = np.array([[convert_str_to_float(pos) for pos in line[1:-1]] for line in lines[2:-3]])
    distances = np.array(spatial.distance.cdist(positions, positions))
    charges = np.array([convert_str_to_float(line[-1]) for line in lines[2:-3]])
    vibrational_freq = lines[-3]
    smiles = dict(zip(["GDB17", "B3LYP"], lines[-2][:-1]))
    inchi = dict(zip(["Corina", "B3LYP"], lines[-1]))
    keys = ["atoms", "positions", "distances", "charges", "vibrational frequencies", "scalar properties", "smiles", "inchi"]
    values = [atoms, positions, distances,  charges, vibrational_freq, scalar_properties, smiles, inchi]
    return dict(zip(keys, values))

def convert_xyz_data(root_dir,filename,target_key):
    mol_dict = format_xyz(root_dir, filename)
    edge_indices, edge_weights = torch_geometric.utils.dense_to_sparse(torch.Tensor(mol_dict["distances"]))
    node_features = np.stack(mol_dict["atoms"], mol_dict["charges"])
    data = torch_geometric.data.Data(x=torch.Tensor(mol_dict["atoms"]), 
                                     edge_index=edge_indices, 
                                     edge_attr=edge_weights,
                                     pos=torch.Tensor(mol_dict["positions"]),
                                     y=torch.Tensor([mol_dict["scalar properties"][target_key]]))
    return data

def format_dataset(root_dir, target_key, target_descr):
    data_name = "QM9_"+str(target_descr)
    raw_dir = os.path.join(root_dir, "raw")
    processed_dir = os.path.join(root_dir, "processed")
    for idx, filename in enumerate(os.listdir(raw_dir)):
        data = convert_xyz_data(root_dir, filename, target_key)
        torch.save(data, os.path.join(processed_dir, data_name+"_{}.pt".format(idx)))



