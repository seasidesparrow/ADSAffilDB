import json

# for testing, use 2025ApJ...978..126Z

'''
Output augments model:
{
  "aff": [
    "University of Lol, Department of General Science, 101 University Way, Anytown, NE 69361; University of Wut, Institute of Physics", # author 1
    "University of Lol, Institute of Chemistry, 102 University Way, Anytown, NE 69361; University of Wut, Institute of Physics" # author 2
  ],
  "aff_abbrev": [
    "ULol/ULol; UWut/IoP",
    "ULol/IoC; UWut/IoP"
  ],
  "aff_canonical": [
    "University of Lol; University of Wut, Institute of Physics",
    "University of Lol, Institute of Chemistry; University of Wut, Institute of Physics",
  ],
  "aff_country": [
    "United States; United States",
    "United States; United States"
  ],
  "aff_facet_hier": [
    "0/ULol",
    "1/ULol/ULol",
    "1/ULol/IoC",
    "0/UWut",
    "1/UWut/IoP"
  ],
  "aff_id": [
    "B01234; B01256",
    "B01235; B01256"
  ],
  "author": [
    "Lehrer, Jim",
    "MacNeil, Bob"
  ],
  "scixID": "SciX:0000-abcd-9876"
}
'''



class AffilFaceter(object):

    def __init__(self):
        pass

    def parse(self, record):
        print("lol.")
        return record
