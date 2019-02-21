#!/usr/bin/python3
from pdbx.reader.PdbxReader import PdbxReader
from pdbx.writer.PdbxWriter import PdbxWriter
from pdbx.reader.PdbxContainers import *
import argparse, gzip, os, fnmatch, shutil

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-i', '--i', dest="incif", help='cif.gz file', required=True)
parser.add_argument('-d', '--d', dest="mmCIFDB", help='mmCIF database diectory', required=True)
parser.add_argument('-o', '--o', dest="outcif", help='mmCIF output', required=True)
args = parser.parse_args()

def find_cif(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern+'*'):
                filename = os.path.join(root, basename)
                with gzip.open(filename, 'rb')as f_in:
                   with open(pattern+'.cif', 'wb') as f_out:
                      shutil.copyfileobj(f_in, f_out)

def open_cif(cif_file):
    """ Assumes a mmCif file and returns a data block used for subsequent procedures """
    # The "usual" procedure to open a mmCIF with pdbX/mmCIF
    with open(cif_file) as cif_fh:
        data = []
        reader = PdbxReader(cif_fh)
        reader.read(data)
        block = data[0]
    return block

def write_cif(container, ocif):
    ofh = open(ocif, 'w')
    pdbxW=PdbxWriter(ofh)
    pdbxW.writeContainer(curContainer)
    ofh.close()

cif_baseName = args.incif.split('_')

find_cif(args.mmCIFDB, cif_baseName[0])

block = open_cif(cif_baseName[0] + '.cif')
os.remove(cif_baseName[0] + '.cif')

curContainer=DataContainer(cif_baseName[0])
#curContainer.append(block.getObj('audit_author'))
#curContainer.append(block.getObj('citation'))

atom_site = block.getObj('atom_site')
atom_site.getRowCount()
aCat=DataCategory("atom_site")
for att in atom_site.getAttributeList():
    aCat.appendAttribute(att)

for atom_row in range(0, atom_site.getRowCount()):
    if(atom_site.getValue('auth_asym_id',atom_row)==cif_baseName[1]) and (atom_site.getValue('group_PDB',atom_row)=='ATOM') and \
        (atom_site.getValue('pdbx_PDB_model_num',atom_row)=='1'):
        atom_site.setValue(cif_baseName[1],'label_asym_id',atom_row)
        aCat.append(atom_site.getFullRow(atom_row))

curContainer.append(aCat)
write_cif(curContainer, args.outcif)
