"""
Functions for counting the occurences of ICD9 codes within a set of
categories.  These can be used for calculating comorbidity scores and
for other reporting functions.
"""

import pandas as pd
import numpy as np


class Counter(object):
    """
    Count matches between subject-associated codes and code categories.

    Parameters
    ----------
    codes_full : dict-like
        A map from category names to lists of ICD9 codes belonging
        to the category.
    codes_initial : dict-like
        A map from category names to list of initial substrings
        of ICD9 codes.  The category will match any code whose
        initial substring matches an element of the list.

    Attributes
    ----------
    table : DataFrame
        A DataFrame whose rows correspond to subjects and columns
        correspond to ICD9 code categories.  The elements of the
        data frame are the number of times a subject was associated
        with a code belonging to the category.

    Notes
    -----
    The motivating use-case is calculating comorbidity scores.

    This class does not perform any standardization or validation of
    the ICD9 codes.  The subject-associated codes must match the
    target codes either exactly (for `full_codes`) or in their initial
    substrings (for `initial_codes`).

    Example
    -------
    Calculate the Elixhauser comorbidity score, defined as the number
    of ICD9 categories in which a subject has at least one reported
    ICD9 code.  `chunk1` and `chunk2` are pandas.Series objects whose
    keys are subject ids, and whose values are ICD9 codes.

    >>> counter = icd9.Counter(codes_full=icd9.elixComorbid)
    >>> counter.update(chunk1)
    >>> counter.update(chunk2)
    >>> elix = (counter.table > 0).sum(1)

    Set up a counter that will count the number of codes per subject
    in two categories.  The first category consists of exactly two
    codes: `12345` and `54321`.  The second category consists of any
    code beginning with the string `44`, and any string beginning with
    the string `323`.

    >>> cat1 = ['12345', '54321']
    >>> cat2 = ['44', '323']
    >>> full = {'group1': cat1}
    >>> init = {'group2': cat2}
    >>> counter = icd9.Counter(codes_full=full, codes_initial=init)
    >>> counter.update(chunk)
    """

    def __init__(self, codes_full=None, codes_initial=None):

        self.codes_full = codes_full if codes_full is not None else {}
        self.codes_initial = codes_initial if codes_initial is not None else {}

        columns = set(self.codes_full.keys()) | set(self.codes_initial.keys())
        columns = list(columns)
        self.table = pd.DataFrame(columns=columns, dtype=np.float64)

        self._matcher = {}
        for col in self.codes_initial:
            f = lambda x : float(any([x.startswith(y) for y in self.codes_initial[col]]))
            self._matcher[col] = f


    def update(self, codes):
        """
        Update the table of ICD9 code counts according to a given set
        of values.

        Parameters
        ----------
        codes : pandas.Series object
            A pandas.Series object whose index contains subject
            identifiers and whose values are ICD9 codes linked to the
            corresponding subject.
        """

        # Add rows for new index values
        ix = np.setdiff1d(codes.index.unique(), self.table.index)
        df = pd.DataFrame(index=ix, dtype=np.float64)
        for col in self.table.columns:
            df[col] = 0.
        self.table = self.table.append(df)

        for col in self.codes_full.keys():
            y = codes.isin(self.codes_full[col]).astype(np.float64)
            s = y.groupby(y.index).agg(np.sum)
            self.table.loc[:, col] = self.table.loc[:, col].add(s, fill_value=0)

        for col in self.codes_initial.keys():
            y = codes.apply(self._matcher[col])
            s = y.groupby(y.index).agg(np.sum)
            self.table.loc[:, col] = self.table.loc[:, col].add(s, fill_value=0)
