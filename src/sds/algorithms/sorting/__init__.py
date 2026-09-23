# Copyright 2024-2026, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Comparison sorts on Python lists.

Both functions accept the same ``key`` and ``reverse`` keywords as the
built-in :func:`sorted`, and both operate on a Python ``list`` only (#93).
They differ in the two properties that distinguish the algorithms:

=================  ====================  ===========  ==============
Function           Result                Stable       Extra space
=================  ====================  ===========  ==============
:func:`merge_sort` new list, input kept  yes          O(n)
:func:`quick_sort` input sorted in place no           O(log n)
=================  ====================  ===========  ==============

To sort the content of a linear structure and get a structure back, go
through :func:`sds.linear.to_list` / :func:`sds.linear.from_list`.

Examples
--------
>>> from sds.algorithms.sorting import merge_sort, quick_sort
>>> merge_sort([3, 1, 2])
[1, 2, 3]
>>> data = [3, 1, 2]
>>> quick_sort(data)
>>> data
[1, 2, 3]
"""

from .merge_sort import merge_sort
from .quick_sort import quick_sort

__all__ = ["merge_sort", "quick_sort"]
