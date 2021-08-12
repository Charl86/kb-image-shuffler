"""Module for creating and managing random sequences or keys."""

import random
from shufflealgos import List


class Key:
    """Class for managing random sequences of integers."""

    def __init__(
            self, globalminval: int = 1, globalmaxval: int = 200,
            length: int = 100, values: List[int] = None) -> None:
        """Build Key object in different ways depending on parameters.

        Parameters
        ----------
        globalminval : int, optional
            The absolute minimum value of the key (not the current
            minimum value in key), defaults to 1
        globalmaxval : int, optional
            The absolute maximum value of the key (not the current
            maximum value in key), defaults to 200 as per one of the
            research papers
        length : int, optional
            The length of the key to be generated if `values` is not
            specified. Defaults to 100 as per one of the research
            papers
        values : List[int], optional
            A user-defined list of integers that will be treated as the
            user key.
        """
        self.__values = values
        self.__globalminval: int = None
        self.__globalmaxval: int = None

        if values is None:
            self.__globalminval = globalminval
            self.__globalmaxval = globalmaxval
            self.__values = self.get_random_key(
                globalminval, globalmaxval, length)
        else:
            self.__values = values.copy()
            if self.__globalminval is None and self.__globalmaxval is None:
                self.__globalminval = min(self.__values)
                self.__globalmaxval = max(self.__values)
            else:
                self.__globalminval = globalminval
                self.__globalmaxval = globalmaxval

    def get_extended_key(self, new_size: int):
        """Return a new key whose size is `new_size`.

        Return a new key whose size is `new_size`, based on the
        the terms of the previous key, and whose new terms are defined
        as shifted values of the canonical terms.
        """
        new_values: List[int] = self.__values.copy()
        next_idx: int = self.length
        range_magnitude: int = self.__globalmaxval - self.__globalminval + 1
        while next_idx < new_size:
            new_term: int = (self.__values[next_idx % self.length]
                             + next_idx // self.length)

            if not self.__globalminval <= new_term <= self.__globalmaxval:
                new_term = (
                    ((new_term - self.__globalminval) % (range_magnitude))
                    + self.__globalminval
                )
            new_values.append(new_term)
            next_idx += 1

        return Key(self.__globalminval, self.__globalmaxval, values=new_values)

    def shift_to_range(self, global_range_min: int, global_range_max: int):
        """Shift the values of the key to the specified range."""
        range_magnitude: int = global_range_max - global_range_min + 1

        new_terms: List[int] = list()
        for term in self.__values:
            new_term = term
            if not global_range_min <= term <= global_range_max:
                if term < global_range_min:
                    new_term = (term % range_magnitude) + global_range_min
                elif term > global_range_max:
                    new_term = (((term - global_range_min) % range_magnitude)
                                + global_range_min)

            new_terms.append(new_term)

        return Key(global_range_min, global_range_max, values=new_terms)

    @property
    def values(self) -> List[int]:
        """Get the key's values."""
        return self.__values

    @property
    def globalminval(self) -> int:
        """Get absolute minimum value of key."""
        return self.__globalminval

    @property
    def globalmaxval(self) -> int:
        """Get absolute maximum value of key."""
        return self.__globalmaxval

    @property
    def localminval(self) -> int:
        """Get the relative minimum value of key."""
        return min(self.__values)

    @property
    def localmaxval(self) -> int:
        """Get the relative maximum value of key."""
        return max(self.__values)

    @property
    def length(self) -> int:
        """Return length of key."""
        return len(self.__values)

    @staticmethod
    def get_random_key(minval: int, maxval: int, length: int) -> List[int]:
        """Generate a random key.

        Parameters
        ----------
        minval: int
            The absolute minimum value of the key
        maxval: int
            The absolute maximum value of the key
        length:
            The desired legnth of the key
        """
        return random.choices(range(minval, maxval + 1), k=length)

    def __str__(self) -> str:
        """Return string representation of key."""
        return f"Key({self.__values})"

    def __repr__(self) -> str:
        """Return object representation of key."""
        return repr(str(self))
