Package reference
=================

This section contents API

.. automodule:: sds


Module core
-----------

.. automodule:: sds.core

Exceptions
``````````

.. automodule:: sds.core.exceptions
   :no-index:

   .. autoexception:: DataStructureError
      :show-inheritance:

   .. autoexception:: EmptyStructureError
      :show-inheritance:

   .. autoexception:: FullStructureError
      :show-inheritance:

   .. autoexception:: InvalidOperationError
      :show-inheritance:

   .. autoexception:: IndexStructureError
      :show-inheritance:

Interfaces
``````````

.. automodule:: sds.core.interfaces

   .. autoclass:: Collection
      :show-inheritance:
      :private-members: __iter__, __contains__, __len__, __bool__

      .. automethod:: clear
      .. automethod:: is_empty

   .. autoclass:: LinearCollection
      :show-inheritance:

      .. automethod:: add
      .. automethod:: remove

Node
````

.. automodule:: sds.core.node

   .. autoclass:: Node
      :show-inheritance:
      :private-members: __repr__, __str__

      .. autoproperty:: data
      .. autoproperty:: next

   .. autoclass:: DoublyNode
      :show-inheritance:
      :private-members: __repr__, __str__

      .. autoproperty:: data
      .. autoproperty:: next
      .. autoproperty:: prev

Module linear
-------------

.. automodule:: sds.linear


Interfaces
``````````

.. automodule:: sds.linear.interfaces

   .. autoclass:: AbstractLinkedList
      :show-inheritance:
      :private-members: __getitem__, __setitem__, __len__

      .. autoproperty:: size
      .. automethod:: prepend
      .. automethod:: append
      .. automethod:: insert_at
      .. automethod:: remove_first
      .. automethod:: remove_last
      .. automethod:: remove_at
      .. automethod:: find
      .. automethod:: reverse
      .. automethod:: add
      .. automethod:: is_empty


Lists
`````

.. automodule:: sds.linear.list

    .. autoclass:: LinkedList
      :show-inheritance:
      :private-members: _get_node, __contains__, __iter__, __getitem__, __setitem__, __len__

      .. autoproperty:: head
      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: append
      .. automethod:: clear
      .. automethod:: find
      .. automethod:: prepend
      .. automethod:: insert_at
      .. automethod:: is_empty
      .. automethod:: remove_at
      .. automethod:: remove_first
      .. automethod:: remove_last
      .. automethod:: reverse

    .. autoclass:: DoublyLinkedList
      :show-inheritance:
      :private-members: _get_node, __contains__, __iter__, __getitem__, __setitem__, __len__

      .. autoproperty:: head
      .. autoproperty:: size
      .. autoproperty:: tail
      .. automethod:: add
      .. automethod:: append
      .. automethod:: clear
      .. automethod:: find
      .. automethod:: prepend
      .. automethod:: insert_at
      .. automethod:: is_empty
      .. automethod:: remove_at
      .. automethod:: remove_first
      .. automethod:: remove_last
      .. automethod:: reverse

    .. autoclass:: CircularLinkedList
      :show-inheritance:
      :private-members: _get_node, __contains__, __iter__, __getitem__, __setitem__, __len__

      .. autoproperty:: head
      .. autoproperty:: tail
      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: append
      .. automethod:: clear
      .. automethod:: find
      .. automethod:: prepend
      .. automethod:: insert_at
      .. automethod:: is_empty
      .. automethod:: remove_at
      .. automethod:: remove_first
      .. automethod:: remove_last
      .. automethod:: reverse

Queues
``````

.. automodule:: sds.linear.queue

   .. autoclass:: PriorityItem
      :show-inheritance:
      :private-members: __lt__, __le__, __gt__, __ge__, __eq__, __repr__, __str__

   .. autoclass:: Queue
      :show-inheritance:
      :private-members: __iter__, __contains__, __len__, __repr__, __str__

      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: clear
      .. automethod:: dequeue
      .. automethod:: enqueue
      .. automethod:: front
      .. automethod:: is_empty
      .. automethod:: rear
      .. automethod:: remove

   .. autoclass:: Deque
      :show-inheritance:
      :private-members: __iter__, __contains__, __len__, __repr__, __str__

      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: add_front
      .. automethod:: add_rear
      .. automethod:: append
      .. automethod:: appendleft
      .. automethod:: clear
      .. automethod:: is_empty
      .. automethod:: peek_front
      .. automethod:: peek_rear
      .. automethod:: pop
      .. automethod:: popleft
      .. automethod:: remove_front
      .. automethod:: remove_rear

   .. autoclass:: PriorityQueue
      :show-inheritance:
      :private-members: __iter__, __contains__, __len__, __repr__, __str__, _compare

      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: clear
      .. automethod:: dequeue
      .. automethod:: enqueue
      .. automethod:: is_empty
      .. automethod:: peek
      .. automethod:: remove

Stacks
``````

.. automodule:: sds.linear.stack

   .. autoclass:: Stack
      :show-inheritance:
      :private-members: __iter__, __contains__, __len__, __repr__, __str__

      .. autoproperty:: size
      .. automethod:: add
      .. automethod:: clear
      .. automethod:: is_empty
      .. automethod:: peek
      .. automethod:: pop
      .. automethod:: push
      .. automethod:: remove
