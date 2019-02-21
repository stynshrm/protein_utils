from pdbx.reader.PdbxReader import PdbxReader
from pdbx.writer.PdbxWriter import PdbxWriter
from pdbx.reader.PdbxContainers import *
import argparse, os

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-i', '--i', dest="incif", help='cif file', required=True)
parser.add_argument('-o', '--o', dest="opdb", help='PDB output', required=True)
args = parser.parse_args()

def open_cif(cif_file):
    """ Assumes a mmCif file and returns a data block used for subsequent procedures """
    # The "usual" procedure to open a mmCIF with pdbX/mmCIF
    with open(cif_file) as cif_fh:
        data = []
        reader = PdbxReader(cif_fh)
        reader.read(data)
        block = data[0]
    return block

block = open_cif(args.incif)
#cif_baseName = args.incif.split('_')
#curContainer = DataContainer(cif_baseName[0])
atom_site = block.getObj('atom_site')

with open(args.opdb, 'w') as ofh:
    for atom_row in range(0, atom_site.getRowCount()):
        at  = atom_site.getValue('group_PDB',atom_row)
        idx = int(atom_site.getValue('id',atom_row))
        atn = atom_site.getValue('label_atom_id',atom_row)
        alt = ""
        res = atom_site.getValue('label_comp_id',atom_row)
        ch  = atom_site.getValue('label_asym_id',atom_row)
        ires= int(atom_site.getValue('label_seq_id',atom_row))
        cir = ""
        x   = float(atom_site.getValue('Cartn_x',atom_row))
        y   = float(atom_site.getValue('Cartn_y',atom_row))
        z   = float(atom_site.getValue('Cartn_z',atom_row))
        occ = float(atom_site.getValue('occupancy',atom_row))
        bf  = float(atom_site.getValue('B_iso_or_equiv',atom_row))
        ele = atom_site.getValue('type_symbol',atom_row)
        chg = ""
        ofh.write("{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}{:2s}\n".format(at,idx, atn, alt, res, ch, ires, cir, x, y, z, occ, bf, ele, chg))
    ofh.write('END')
