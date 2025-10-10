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
  "aff_facet_hier": [
    "0/ULol",
    "1/ULol/ULol",
    "1/ULol/IoC",
    "0/UWut",
    "1/UWut/IoP"
  ],
  "author": [
    "Lehrer, Jim",
    "MacNeil, Bob"
  ],
  "scixID": "SciX:0000-abcd-9876"
}
'''



class AffilAugmenter(object):

    def __init__(self):
        pass

        
    def _build_aff_id(self):
    # "aff_id": [
    #   "B01234; B01256",
    #   "B01235; B01256"
    # ],
        aff_id = []
        for auth in self.author_data:
            author_affid_string = "; ".join([a.get("inst_id", "-") for a in auth])
            aff_id.append(author_affid_string)
        self.aff_id = aff_id

    def _build_aff_canonical(self):
    # "aff_canonical": [
    #   "University of Lol; University of Wut, Institute of Physics",
    #   "University of Lol, Institute of Chemistry; University of Wut, Institute of Physics",
    # ],
        aff_canonical = []
        for auth in self.author_data:
            author_canonical_string = "; ".join([a.get("inst_canonical", "-") for a in auth])
            aff_canonical.append(author_canonical_string)
        self.aff_canonical = aff_canonical

    def _build_aff_country(self):
    # "aff_country": [
    #   "United States; United States",
    #   "United States; United States"
    # ],
        aff_country = []
        for auth in self.author_data:
            author_country_string = "; ".join([a.get("inst_country", "-") for a in auth])
            aff_country.append(author_country_string)
        self.aff_country = aff_country

    def _build_facets(self):
        for auth in self.author_data:
            for aff in auth:
                print("%s" % json.dumps(aff, indent=2, sort_keys=True))
                canonical_string = aff.get("inst_canonical", "-")
                aff_id = aff.get("inst_id", "-")
                aff_abbrev = aff.get("inst_abbreviation", "-")
                aff_country = aff.get("inst_country", "-")
                aff_parents = aff.get("parent_data", [])
                for p in aff_parents:
                    parent_abbrev = p.get("inst_abbreviation", "-")

    def _build_output(self):
        self.aff = self.record.get("aff", [])
        #self._build_aff_canonical()
        #self._build_aff_country()
        #self._build_aff_id()
        self._build_facets()
        self.author = self.record.get("author", [])
        self.bibcode = self.record.get("bibcode", "")
        self.scixID = self.record.get("scixID", "")
        self.output = {
            "aff": self.aff,
            "aff_country": self.aff_country,
            "aff_canonical": self.aff_canonical,
            "aff_id": self.aff_id,
            "author": self.author,
            "bibcode": self.bibcode,
            "scix_id": self.scixID
        }

    def parse(self, record, author_data):
        self.record = record
        self.author_data = author_data
        self._build_output()
        return self.output
