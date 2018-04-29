import json
from typing import Dict, NewType, List

Association = NewType("Association", dict)
# Entity = NewType("Entity", dict)

class Entity(dict):

    def __init__(self, d):
        super(Entity, self).__init__(d)

    def __hash__(self):
        id = self.get("id", 1).__hash__()
        label = self.get("label", 1).__hash__()
        name = self.get("full_name", 1).__hash__()
        synonyms = self.get("synonyms", None)
        synhash = 1
        if synonyms is not None:
            for i, syn in enumerate(synonyms):
                synhash = 2 ** i * syn.__hash__() + synhash

        t = self.get("type", 1)
        taxon = self.get("taxon", 1).get("id", 1).__hash__()

        return id * label * name * synhash * t * taxon



class GafGpiBridge(object):

    def __init__(self):
        self.cache = []

    def convert_association(self, association: Association) -> Entity:
        """
        'id' is already `join`ed in both the Association and the Entity,
        so we don't have to worry about what that looks like. We assume
        it's correct.
        """
        if "header" not in association or association["header"] == False:
            # print(json.dumps(association, indent=4))
            gpi_obj = {
                'id': association["subject"]["id"],
                'label': association["subject"]["label"],  # db_object_symbol,
                'full_name': association["subject"]["fullname"],  # db_object_name,
                'synonyms': association["subject"]["synonyms"],
                'type': association["subject"]["type"], #db_object_type,
                'parents': "", # GAF does not have this field, but it's optional in GPI
                'xrefs': "", # GAF does not have this field, but it's optional in GPI
                'taxon': {
                    'id': association["subject"]["taxon"]["id"]
                }
            }
            return gpi_obj

        return None

    def entities(self) -> List[Entity]:
        return list(self.cache)
