"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""

import cmath
import math
from numpy import NAN

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        required params
        pdes (str)
        name (str)
        full_name (str)
        pha (bool)

        optional
        diameter (float)

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        self.designation = info['pdes'].strip()
        self.full_name = info['full_name'].strip()
        if not info['name']:
            self.name = None
        else:
            self.name = info['name'].strip().replace('"', '')
        if info['diameter']:
            self.diameter = float(info['diameter'])
        else:
            self.diameter = cmath.nan
        if info['pha'].lower() == 'y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.full_name}'

    def __str__(self):
        """Return `str(self)`."""
        # Returns a human-readable string representation
        if self.hazardous:
            isNot = ''
        else:
            isNot = 'not '
        if type(self.diameter) == float:
            diamString = f'a diameter of {self.diameter:.3f} km'
        else:
            diamString = 'an unknown diameter'
        return f'NEO {self.full_name!r} has {diamString} and is {isNot}potentially hazardous.' \

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        if type(self.diameter) == float:
            diamString = f'{self.diameter:.3f}'
        else:
            diamString = 'UNKNOWN'
        return f"NearEarthObject(designation={self.designation!r}, " \
               f"diameter={diamString}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        required parameters
        des (str) _designation (from CAD / tentative)
        cd (str) date and time
        dist_min (float) min distance in AU
        v_rel (float) km/s velocity rel to approach body at close approach 

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """       
        self.time = cd_to_datetime(info['cd'])
        self.distance = float(info['dist_min'])
        self.velocity = float(info['v_rel'])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

        # This is used until neo can be populated with an object ref
        self._designation = info['des'].strip()

    @property
    def temp_designation(self):
        return self._designation

    @property
    def designation(self):
        return self.designation
    
    @designation.setter
    def designation(self, des):
        self.designation = des

    @designation.getter
    def designation(self):
        return self.designation

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # TODO: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        #return f'At {datetime_to_str(self.time)}, {self.full_name} approaches Earth at a distance of ' \
        if not math.isnan(self.neo.diameter):
            return f'{datetime_to_str(self.time)}, {self._designation} ({self.neo.diameter} km diameter) approaches at a distance of ' \
                f'{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s. '
        else:
            return f'{datetime_to_str(self.time)}, {self._designation} (diameter unknown) approaches at a distance of ' \
                f'{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s. '

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
    
    # Suitable for CSV
    @property
    def exportName(self):
        if self.neo.name:
            return self.neo.name
        else:
            return '""'

    # Suitable for JSON
    @property
    def exportJsonName(self):
        if self.neo.name:
            return f'{self.neo.name}'
        else:
            return str('')


    # Suitable for CSV
    @property
    def exportDiam(self):
        if math.isnan(self.neo.diameter) or self.neo.diameter == None:
            return '""'
        else:
            return self.neo.diameter

    # Suitable for JSON
    @property
    def exportJsonDiam(self):
        if math.isnan(self.neo.diameter) or self.neo.diameter == None:
            return float(0)
        else:
            return self.neo.diameter

    # this returns a collection suitable for dumping straight in to CSV writer
    @property
    def csvMaker(self):
        return (
            self.time.strftime("%Y-%m-%d %H:%M"),
            self.distance,
            self.velocity,
            self.neo.designation,
            self.exportName,
            self.exportDiam,
            self.neo.hazardous
        )
    
    # This returns a dict ready to be added to JSON
    @property
    def jsonMaker(self):
        return {'datetime_utc': self.time.strftime("%Y-%m-%d %H:%M"),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': {
                'designation': self.neo.designation,
                'name': self.exportJsonName,
                'diameter_km': self.exportJsonDiam,
                'potentially_hazardous': self.neo.hazardous
            }
        }