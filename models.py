"""NEO and approach object model module for NearEarthObjects."""

import cmath
import math
from numpy import NAN

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """Represents one NEO from the input file."""

    def __init__(self, **info):
        """Create a new NearEarthObject.

        required:
        pdes (str)
        name (str)
        full_name (str)
        pha (bool)

        optional
        diameter (float)
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
        """Return a human-readable string representation."""
        if self.hazardous:
            isNot = ''
        else:
            isNot = 'not '
        if type(self.diameter) == float:
            diamString = f'a diameter of {self.diameter:.3f} km'
        else:
            diamString = 'an unknown diameter'
        return f'NEO {self.full_name!r} has {diamString} ' + \
            f'and is {isNot}potentially hazardous.'

    def __repr__(self):
        """Return a code-like string representation of this object."""
        if type(self.diameter) == float:
            diamString = f'diameter={self.diameter:f} (optional), '
        else:
            diamString = ''
        return f'NearEarthObject(pdes={self.designation!r}, ' \
            f'name={self.name!r}, ' + \
            f'full_name={self.full_name}, ' + \
            diamString + \
            f'pha={self.hazardous})'


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, **info):
        """Create a new CloseApproach object.

        Required parameters
        des (str) _designation (from CAD / tentative)
        cd (str) date and time
        dist_min (float) min distance in AU
        v_rel (float) km/s velocity rel to approach body
        """
        self.time = cd_to_datetime(info['cd'])
        self.distance = float(info['dist_min'])
        self.velocity = float(info['v_rel'])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

        # This is used until neo can be populated with an object ref
        self._designation = info['des'].strip()

    def __str__(self):
        """Return human readable string representation."""
        # the wording is different if diameter is undefined.
        if not math.isnan(self.neo.diameter):
            return f'{datetime_to_str(self.time)}, ' + \
                f'{self._designation} ' + \
                f'({self.neo.diameter} km ' + \
                f'diameter) approaches at a distance of ' + \
                f'{self.distance:.2f} au and a velocity of ' + \
                f'{self.velocity:.2f} km/s.'
        else:
            return f'{datetime_to_str(self.time)}, ' + \
                f'{self._designation} ' + \
                f'(diameter unknown) approaches at a distance of ' + \
                f'{self.distance:.2f} au and a velocity of ' + \
                f'{self.velocity:.2f} km/s.'

    def __repr__(self):
        """Return code-like string representation."""
        return f'CloseApproach(des={self._designation!r}, ' + \
            f'cd={datetime_to_str(self.time)!r}, ' + \
            f'dist_min={self.distance:f}, ' + \
            f'v_rel={self.velocity:f})'

    @property
    def exportName(self):
        """Return name formatted for CSV export."""
        if self.neo.name:
            return self.neo.name
        else:
            return '""'

    @property
    def exportJsonName(self):
        """Return name formatted for JSON export."""
        if self.neo.name:
            return f'{self.neo.name}'
        else:
            return str('')

    @property
    def exportDiam(self):
        """Return diameter formatted for CSV export."""
        if math.isnan(self.neo.diameter) or self.neo.diameter is None:
            return '""'
        else:
            return self.neo.diameter

    @property
    def exportJsonDiam(self):
        """Return diameter formatted for JSON export."""
        if math.isnan(self.neo.diameter) or self.neo.diameter is None:
            return float(0)
        else:
            return self.neo.diameter

    @property
    def csvMaker(self):
        """Return a collection ready for one line of CSV export."""
        return (
            self.time.strftime("%Y-%m-%d %H:%M"),
            self.distance,
            self.velocity,
            self.neo.designation,
            self.exportName,
            self.exportDiam,
            self.neo.hazardous
        )

    @property
    def jsonMaker(self):
        """Return a dict ready to be added to (pre)JSON collection."""
        return {
                'datetime_utc': self.time.strftime("%Y-%m-%d %H:%M"),
                'distance_au': self.distance,
                'velocity_km_s': self.velocity,
                'neo': {
                    'designation': self.neo.designation,
                    'name': self.exportJsonName,
                    'diameter_km': self.exportJsonDiam,
                    'potentially_hazardous': self.neo.hazardous
                }
        }
