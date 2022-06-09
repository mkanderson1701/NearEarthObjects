import operator
from itertools import islice
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""

class AttributeFilter:
    """A general superclass for filters on comparable attributes."""
    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from an binary predicate and a reference value.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


class DistanceFilter(AttributeFilter):
    def __init__(self, op, value):
        super().__init__(op, value)
    
    def __call__(self, approach):
        return self.op(approach.distance, self.value)

    @classmethod
    def get(cls, approach):
        return approach.distance

    @classmethod
    def validateDist(cls, val):
        try:
            val = float(val)
        except UnsupportedCriterionError as err:
            print('distance filter could not be converted to float', err)
        return val
            

class DateFilter(AttributeFilter):
    def __init__(self, op, value):
        super().__init__(op, value)
    
    def __call__(self, approach):
        return self.op(approach.time.date(), self.value)

    @classmethod
    def get(cls, approach):
        return approach.time.date()


class VelocityFilter(AttributeFilter):
    def __init__(self, op, value):
        super().__init__(op, value)
    
    def __call__(self, approach):
        return self.op(approach.velocity, self.value)

    @classmethod
    def get(cls, approach):
        return approach.velocity


class DiameterFilter(AttributeFilter):
    def __init__(self, op, value):
        super().__init__(op, value)
    
    def __call__(self, approach):
        return self.op(approach.neo.diameter, self.value)

    @classmethod
    def get(cls, approach):
        return approach.neo.diameter

class HazardFilter(AttributeFilter):
    def __init__(self, op, value):
        super().__init__(op, value)
    
    def __call__(self, approach):
        return self.op(approach.neo.hazardous, self.value)

    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    # assembles a collection of filters
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
    if not hazardous == None:
        filters.append(HazardFilter(operator.eq, hazardous))

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.
    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    # Used islice as recommended
    if n == 0:
        n = None
    for item in islice(iterator, 0, n):
        yield item
