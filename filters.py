"""Search filter creation module for NearEarthObjects."""

import operator
from itertools import islice
import logging
import sys


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes."""

    def __init__(self, op, value):
        """Construct a new "AttributeFilter".

        :param op: A 2-argument predicate comparator (such as "operator.le").
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Return an expression to test the two values.

        class method "get" is overridden in each subclass
        to provide the correct value.
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        :param approach: A "CloseApproach" on to evaluate.
        :return: The value of an attribute of interest.

        This is overridden in the subclasses to return actual
        property of interest.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return code-like string representation."""
        return f'{self.__class__.__name__}' + \
            f'(op=operator.{self.op.__name__},' + \
            f'value={self.value})'


class DistanceFilter(AttributeFilter):
    """Class for filtering approaches by distance."""

    def __init__(self, op, value):
        """Construct a new DistanceFilter.

        :param op: A 2-argument predicate comparator (such as "operator.le").
        :param value: The reference value to compare against.
        """
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Return distance from this approach."""
        return approach.distance

    @classmethod
    def validateDist(cls, val):
        """Convert to float and check validity of distance to be tested."""
        try:
            val = float(val)
        except UnsupportedCriterionError as err:
            print('distance filter could not be converted to float', err)
        return val


class DateFilter(AttributeFilter):
    """Class for filtering approaches by date."""

    def __init__(self, op, value):
        """Construct a new DateFilter.

        :param op: A 2-argument predicate comparator (such as "operator.le").
        :param value: The reference value to compare against.
        """
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Return date of this approach."""
        return approach.time.date()


class VelocityFilter(AttributeFilter):
    """Class for filtering approaches by velocity."""

    def __init__(self, op, value):
        """Construct a new VelocityFilter.

        :param op: A 2-argument predicate comparator (such as "operator.le").
        :param value: The reference value to compare against.
        """
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Return velocity at this approach."""
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Class for filtering approaches by diameter."""

    def __init__(self, op, value):
        """Construct a new DiameterFilter.

        :param op: A 2-argument predicate comparator (such as "operator.le").
        :param value: The reference value to compare against.
        """
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Return diameter of neo associated with this approach."""
        return approach.neo.diameter


class HazardFilter(AttributeFilter):
    """Class for filtering approaches by hazard status."""

    def __init__(self, op, value):
        """Construct a new HazardFilter.

        :param op: A 2-argument predicate comparator.
        :param value: The reference value to compare against.

        For hazardfilter the comparator will be operator.eq
        """
        super().__init__(op, value)

    @classmethod
    def get(cls, approach):
        """Return hazardous status of neo associated with this approach."""
        return approach.neo.hazardous


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None):
    """Assemble a collection of filters.

    optional keyword arguments:
    date: (datetime) exact date of approach
    start_date: (datetime) minimum approach date
    end_date: (datetime) max approach date
    distance_min: (number) minimum approach distance
    distance_max: (number) maximum approach distance
    velocity_min: (number) minimum approach velocity
    velocity_max: (number) maximum approach velocity
    diameter_min: (number) minimum NEO diameter
    diameter_max: (number) maximum NEO diameter
    hazardous: boolean. Is associated neo potentially hazardous

    Returns collection of filter expressions.
    """
    filters = []

    if distance_min:
        distance_min = DistanceFilter.validateDist(distance_min)
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        distance_max = DistanceFilter.validateDist(distance_max)
        filters.append(DistanceFilter(operator.le, distance_max))
    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))
    if velocity_min:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardFilter(operator.eq, hazardous))
    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) "n" values from the iterator.
    """
    # Used islice as recommended
    if n == 0:
        n = None
    for item in islice(iterator, 0, n):
        yield item
