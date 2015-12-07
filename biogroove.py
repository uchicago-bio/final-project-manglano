import pdbatoms, rmsd, sys, pysynth as giorgio

"""
   Biogroove v0.1: Generative Music Synthesis Seeded by Protein Sequences
                    A Proof of Concept By David J. Manglano
   Depends Upon: boscoh's pdbremix (https://github.com/boscoh/pdbremix)
                 mdoege's pysynth (github.com/mdoege/PySynth)
   Dedicated to: Brian Eno, Rosalind Franklind, Linus Pauling, MCA, H.R. Giger
   Powered by  : Tarot cards, coffee, & Koyaanisqatsi.
   And so      : Let's Rock.
"""
alphaPrecedes = 0
betaPrecedes = 0

def motifTune(motifRes):
    alphaMotif = (("f",-4),("r",-8),("a",-8),("c",-8),("a",-4))
    betaMotif  = (("d",-4),("r",-8),("f",-8),("a",-8),("d",-4))
    theHeatGoesOn = (("c",-4),("r",8),("a",-4),("f",-8))
    #recognize alpha-helix
    malek = ["M","A","L","E","K"]
    alphaCounter=0
    #recognize beta-sheet
    tyvfiw = ["T","Y","V","F","I","W"]
    betaCounter=0
    loopCounter=0
    global alphaPrecedes
    global betaPrecedes

    for item in motifRes:
        if item in malek:
            alphaCounter+=1
        elif item in tyvfiw:
            betaCounter+=1
        else:
            loopCounter+=1
    if alphaCounter >= 5:
        print("Helix!")
        ##cache the current "arpeggiator dial"
        cacheBool = alphaPrecedes
        ##update the settings to influence the next motif
        alphaPrecedes += 1
        if betaPrecedes > 0:
            betaPrecedes = 0
        return shiftMotif(alphaMotif, "a",cacheBool)
    if betaCounter >= 5:
        print("Sheet!")
        ##cache the current "arpeggiator dial"
        cacheBool = betaPrecedes
        ##update the settings to influence the next motif
        betaPrecedes += 1
        if alphaPrecedes > 0:
            alphaPrecedes = 0
        return shiftMotif(betaMotif,"b",cacheBool)
    else:
        print("Loop!")
        ##loops get a static, tired track
        return theHeatGoesOn

def shiftMotif(motif,motifType,inMotif):
    if motifType == "a":
        if (inMotif == 0):
            return motif
        elif (inMotif < 3):
            return (("f",-8),("r",16),("f",16),("c",-8),("a",-8),("d",-4))
        else:
            return (("f",-4),("r",-8),("f",16),("c",1),("a",8))
    else:
        if (inMotif == 0):
            return motif
        elif (inMotif < 3):
            return (("d",-8),("r",8),("f",-8),("a",1),("d",1))
        else:
            return (("d",1),("r",-8),("f",1),("a",8),("d",-8),("a",8))


##map PDB 3-character amino codes to 1-character codes
threeToOne = {"GLY" : "G", "PRO" : "P","ALA" : "A","VAL" : "V","LEU" : "L",
"ILE" : "I","MET" : "M","CYS" : "C","PHE" : "F","TYR" : "Y","TRP" : "W",
"HIS" : "H","LYS" : "K","ARG" : "K","TYR" : "Y","TRP" : "W","HIS" : "H",
"LYS" : "K","ARG" : "R","GLN" : "Q","ASN" : "N","GLU" : "E","ASP" : "D",
"SER" : "S","THR" : "T"}

##specify a protein path
proteinPath = "5E6E.pdb"
proteinSoup = pdbatoms.Soup(proteinPath)
atomList  = rmsd.get_superposable_atoms(proteinSoup,None,['CA'])

#functionally generate single-character codes from a pdb
atomCodes = map (lambda y: threeToOne[y],map(lambda x: x.res_type,atomList))

#generate sublists for the music functions, best done with a for loop as far as i know
sublists = []
for index in range(0, len(atomCodes) - 10):
        sublists.append(atomCodes[index:index+10])

#make a music box: feed in the sublists and process them with motifTune
whereIComeFromTheBirdsSingAPrettySong = map(lambda x: motifTune(x),sublists)

#read the notes of each sublist tune into a single tune
andTheresAlwaysMusicInTheAir = []
for item in whereIComeFromTheBirdsSingAPrettySong:
    for note in item:
        andTheresAlwaysMusicInTheAir.append(note)
giorgio.make_wav(andTheresAlwaysMusicInTheAir,bpm=300,fn=proteinPath[:len(proteinPath)-4] + ".wav")
