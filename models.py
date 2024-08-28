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
from helpers import cd_to_datetime, datetime_to_str
import math

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
    def __init__(self, designation, name, diameter, hazardous):
        """Create a new `NearEarthObject`.

        :param designation: A string with unique identifier for near earth object(neo)
        :param name: A string with common name of neo, not all neos have a common name, so may receive empty string
        :param diameter: A string with diameter of the neo, not all data has a diameter so may receive empty string
        :param hazardous: A string with values Y for hazardous and N for not hazardous
        """
        self.designation = designation

        if name:
            self.name = name
        else:
            self.name = None

        if diameter:
            self.diameter = float(diameter)
        else:
            self.diameter = float('nan')
        
        if hazardous == 'Y':
            self.hazardous = True
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} - {self.name}"

    def __str__(self):
        """Return `str(self)`."""
        return f"{self.fullname}, has a diameter of {'not available' if math.isnan(self.diameter) else self.diameter:.3f}, and {'is' if self.hazardous else 'is not'} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
    
    def serialize(self):
        """Returns a dictionary of attributes for CSV or JSON serialization
        
        Fields are 'designation', 'name', 'diameter_km', 'potentially_hazardous'
        Missing names are repesented by empty strings
        """
        attributes = {}

        attributes['designation'] = self.designation

        if self.name:
            attributes['name'] = self.name
        else:
            attributes['name'] = ''
        
        attributes['diameter_km'] = self.diameter
        attributes['potentially_hazardous'] = self.hazardous
        
        return attributes
        
                

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
    def __init__(self, designation, time, distance, velocity):
        """Create a new `CloseApproach`.

        :param designation: A string with unique identifier for near earth object(neo)
        :param time: string, date and time, in UTC, at which the neo passes closest to earth
        :param distance: string, the nominal approach distance, in astronomical units, of the neo to the earth at the closest point
        :param velocity: string, the velocity, in kilometers per second, of the NEO relative to earth at the closet point
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

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
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, {self.neo.fullname} approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """Returns a dictionary of attributes for CSV or JSON serialization
        
        Fields are 'datetime_utc', 'distance_au', 'velocity_km_s' 
        """
        
        attributes = {}

        attributes['datetime_utc'] = datetime_to_str(self.time)
        attributes['distance_au'] = self.distance
        attributes['velocity_km_s'] = self.velocity

        return attributes        
