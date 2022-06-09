import time


def binarySearch(arr, l, r, x):
    """
    This is useful after the neo list is sorted by designation.

    Simple recursive binary search implementation found at:

    https://www.geeksforgeeks.org/binary-search/ 
    
    A recursive binary search function. It returns
    location of x in given array arr[l..r] is present,
    otherwise -1 
    """

     # Check base case
    if r >= l:
        mid = l + (r - l) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid-1, x)

        # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)
 
    else:
        # Element is not present in the array
        return -1


class NEODatabase:
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        print('Building database...\n')

        # Additional data structures and optimizations

        # _neos_named
        # 
        # dict of neos with a non-empty name property
        # basically a hash table
        # for quick searches by name
        self._neos_named = {}
        for neo in neos:
            if not neo.name == None and not neo.name == '':
                self._neos_named[neo.name] = neo

        # sort neos by designation
        # permits binary search against designations 

        self._neos.sort(key=lambda x: x.designation)

        # neos designation array. for fast search against designations.
        #
        # I can do a binary search against this list then match the index to the full object collection.
        
        self.neo_designations = []
        for neo in self._neos:
            self.neo_designations.append(neo.designation)
        self.neo_designations_len = len(self.neo_designations) - 1

        # This dict will have one index per NEO
        # Each index then has a list of matching approaches.

        self._approach_des_dict = {}
        for approach in approaches:

            # create dictionary / hash table
            # {designation (str) : [list of approach objects]}

            # If index (designation) already exists, append
            if approach._designation in self._approach_des_dict:
                self._approach_des_dict[approach._designation].append(approach)
            # If not, add with new index
            else:
                self._approach_des_dict[approach._designation] = [approach]
            
            # Use binary search to find the matching NEO designation

            neoIndex = binarySearch(self.neo_designations, 0,
                self.neo_designations_len, approach._designation)

            # Now add the real links between NEO and approach objects

            approach.neo = self._neos[neoIndex]
            self._neos[neoIndex].approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """
        Grab a neo by designation
        """
        neoIndex = binarySearch(self.neo_designations, 0, 
            self.neo_designations_len, designation)
        if neoIndex != -1:
            return self._neos[neoIndex] # works because _neos is sorted and mated to neo_designations


    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.
        """
        if name == None or name == '':
            return None

        # Returns None if not in dictionary
        try:
            return self._neos_named[name]
        except:
            return None


    def query(self, filters=()):
        for approach in self._approaches:
            passedFilters = True
            # eliminate this approach if it doesn't pass a filter
            for filter in filters:
                if not filter(approach):
                    passedFilters = False
                    break # stop checking any remaining filters
            # if passed, yield
            if passedFilters:
                yield approach
