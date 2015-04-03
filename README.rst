This is a Python implementation of some of the features of the R icd9_
package.

_icd9: http://cran.r-project.org/web/packages/icd9/index.html

ICD9 is version 9 of the "International Statistical Classification of
Diseases and Related Health Problems".  See
http://en.wikipedia.org/wiki/ICD for more information.

The package includes lists of ICD9 codes associated with specific
conditions, and information about the ICD9 codes themselves.

::

  >>> import icd9
  >>> codes1 = icd9.ahrqComorbidAll
  >>> codes2 = icd9.elixComorbid
  >>> codes3 = icd9.icd9Hierarchy
  >>> codes4 = icd9.ahrqComorbid
  >>> codes5 = icd9.icd9Chapters
  >>> codes6 = icd9.quanElixComorbid

The package contains functions for manipulating the codes.

::

  >>> icd9.decimal_to_short("81.23")
  "08123"
  >>> icd9.short_to_decimal("08123")
  "81.23"
  >>> icd9.decimal_to_parts("9.9")
  ("009", "9")
  >>> icd9.parts_to_decimal("088", "88")
  "88.88"
  >>> icd9.short_to_parts("E0123")
  ("E012", "3")
  >>> icd9.parts_to_short("V1", "0")
  "V010"
  >>> icd9.parts_to_short("E012", "3")
  "E0123"

The package contains a ``Counter`` class for determining the number of
times a given subject has codes that belong to one or more classes.
To illustrate, first we define a class that contains the codes '12345'
and '54321', and a second class that contains all codes beginning with
'44' and all codes beginning with '323':

::

  >>> full = {"group1": ["12345", "54321"]
  >>> init = {"group2": ["44", "323"]}
  >>> counter = icd9.Counter(codes_full=full, codes_initial=init)

Now we can take a ``Pandas.Series`` object `codes` whose index is
interpreted as subject identifiers, and whose values are ICD9 codes,
and update the counter:

::

  >>> counter.update(codes)

The ``counter.table`` attribute contains the number of occurences of
each code within each of the groups, in each subject.

All of the data components of the package were obtained from the R
icd9 package.  See COPYRIGHT.txt for relevant copyright information.
The R script used to prepare the JSON files distributed with this
package can be found in the ``resources`` subdirectory.

See also https://github.com/sirrice/icd9.
