"""Database module for NearEarthObjects."""

import time


def binarySearch(arr, left, right, search):
    """Recursive binary search implementation.

    Borrowed from:
    https://www.geeksforgeeks.org/binary-search/

    Arguments:
    arr -- the SORTED collection to be searched
    left -- index of leftmost boundary
    right -- index of rightmost boundary
    search -- value to be located

    Returns:
    If located: index of value in collection
    If not found: -1
    """
    if right >= left:
        mid = left + (right - left) // 2

        # If element is present at the middle itself
        if arr[mid] == search:
            return mid

        # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > search:
            return binarySearch(arr, left, mid-1, search)

        # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, right, search)

    else:
        # Element is not present in the array
        return -1


class NEODatabase:
    """Database of NEOs and approaches."""

    def __init__(self, neos, approaches):
        """Create a new NEODatabase.

        Arguments:
        neos: A collection of NearEarthObjects from extract.py
        approaches: A collection of CloseApproaches from extract.py

        immediately does some sorting and provides search interfaces.
        """
        # neos may arrive cast as a tuple (i.e. test_write.py for no reason)

        self._neos = list(neos)  # correct it back to a list for sorting.
        self._approaches = approaches  # _approaches can be a tuple if it wants

        print('Building database...\n')

        # sorting permits binary search against designations
        self._neos.sort(key=lambda x: x.designation)

        """"_neos_named
        dict of all neos with a non-empty name property
        a hash table for quick searches by name
        """
        self._neos_named = {}
        for neo in neos:
            if neo.name is not None and neo.name != '':
                self._neos_named[neo.name] = neo

        """neo_designations
        neo designations only.
        ordering matches full _neos list
        find a designation in this with binary search
        then retrieve the neo with same index in _neos
        """
        self.neo_designations = []
        for neo in self._neos:
            self.neo_designations.append(neo.designation)
        self.neo_designations_len = len(self.neo_designations) - 1

        """ The following approach loop accomplishes two things.

        Builds dictionary of unique designations to approaches
        While a neo object has the same list, this dict is a faster lookup
        if you have the designation.

        {designation (str) : [list of approach objects]}

        Sets up list of approaches in the neo objects, and the links
        to neo objects in the approaches
        """
        self._approach_des_dict = {}
        for approach in approaches:

            # If index (designation) already exists, append
            if approach._designation in self._approach_des_dict:
                self._approach_des_dict[approach._designation].append(approach)
            # If not, add with new index
            else:
                self._approach_des_dict[approach._designation] = [approach]

            # Use binary search to find the matching NEO designation
            neoIndex = binarySearch(self.neo_designations, 0,
                                    self.neo_designations_len,
                                    approach._designation)

            # Now add the real links between NEO and approach objects
            approach.neo = self._neos[neoIndex]
            self._neos[neoIndex].approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Search by designation and return NearEarthObject."""
        neoIndex = binarySearch(self.neo_designations, 0,
                                self.neo_designations_len, designation)
        if neoIndex != -1:
            # _neos is sorted and mated to neo_designations
            return self._neos[neoIndex]

    def get_neo_by_name(self, name):
        """Search by name and return NearEarthObject."""
        # test for very bad name parameter
        if name is None or name == '':
            return None
        # check the dict
        try:
            return self._neos_named[name]
        # Returns None if not in dictionary
        except KeyError as err:
            return None

    def query(self, filters=()):
        """Create a close approach iterator with filtered results.

        Keyword argument (optional):
        filters: a collection of filter objects from filters.py

        yields close approaches passing any filters.
        """
        for approach in self._approaches:
            passedFilters = True

            # eliminate this approach if it doesn't pass a filter
            for filter in filters:
                if not filter(approach):
                    passedFilters = False
                    break  # stop checking any remaining filters

            # if passed, yield
            if passedFilters:
                yield approach

    def __str__(self):
        """Human-readable string representation."""
        print(f'NEODatabase containing {len(self.neo_designations)} \
            NEOs and {len(self.approaches)} approaches.')

    def __repr__(self):
        """Code-like representation."""
        return f'NEODatabase({self._neos}, \
            {self._approaches}'
