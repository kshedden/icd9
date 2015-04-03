import icd9
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

cat1 = ["12345", "54321"]
cat2 = ["44", "323"]
full = {"group1": cat1}
init = {"group2": cat2}
counter = icd9.Counter(codes_full=full, codes_initial=init)

chunk = pd.Series(["12345", "12345", "32", "441", "54321"], [1, 2, 3, 4, 5])
counter.update(chunk)

chunk = pd.Series( ["12345", "440", "32", "441", "54321"], [1, 2, 5, 6, 6])
counter.update(chunk)

expected = pd.DataFrame([[2, 0], [1, 1], [0, 0], [0, 1], [1, 0], [1, 1]],
                        index=[1, 2, 3, 4, 5, 6], dtype=np.float64,
                        columns=["group1", "group2"])

assert_frame_equal(counter.table, expected)


