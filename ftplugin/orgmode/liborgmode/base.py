# -*- coding: utf-8 -*-

"""
    base
    ~~~~~~~~~~

    Here are really basic data structures that are uset througout the liborgmode.
"""

from UserList import UserList


def flatten_list(l):
	res = []
	if type(l) in (tuple, list) or isinstance(l, UserList):
		for i in l:
			if type(i) in (list, tuple) or isinstance(i, UserList):
				res.extend(flatten_list(i))
			else:
				res.append(i)
	return res


class Direction():
	FORWARD = 1
	BACKWARD = 2


class MultiPurposeList(UserList):
	u""" A Multi Purpose List is a list that calls a user defined hook on
	change. The impelementation is very basic - the hook is called without any
	parameters. Otherwise the Multi Purpose List can be used like any other
	list.

	The member element "data" can be used to fill the list without causing the
	list to be marked dirty. This should only be used during initialization!
	"""

	def __init__(self, initlist=None, on_change=None):
		UserList.__init__(self, initlist)
		self._on_change = on_change

	def _changed(self):
		u"""
		Call hook
		"""
		if callable(self._on_change):
			self._on_change()

	def __setitem__(self, i, item):
		UserList.__setitem__(self, i, item)
		self._changed()

	def __delitem__(self, i):
		UserList.__delitem__(self, i)
		self._changed()

	def __setslice__(self, i, j, other):
		UserList.__setslice__(self, i, j, other)
		self._changed()

	def __delslice__(self, i, j):
		UserList.__delslice__(self, i, j)
		self._changed()

	def __getslice__(self, i, j):
		# fix UserList - don't return a new list of the same type but just the
		# normal list item
		i = max(i, 0); j = max(j, 0)
		return self.data[i:j]

	def __iadd__(self, other):
		res = UserList.__iadd__(self, other)
		self._changed()
		return res

	def __imul__(self, n):
		res = UserList.__imul__(self, n)
		self._changed()
		return res

	def append(self, item):
		UserList.append(self, item)
		self._changed()

	def insert(self, i, item):
		UserList.insert(self, i, item)
		self._changed()

	def pop(self, i=-1):
		item = self[i]
		del self[i]
		return item

	def remove(self, item):
		self.__delitem__(self.index(item))

	def reverse(self):
		UserList.reverse(self)
		self._changed()

	def sort(self, *args, **kwds):
		UserList.sort(self, *args, **kwds)
		self._changed()

	def extend(self, other):
		UserList.extend(self, other)
		self._changed()


# vim: set noexpandtab:
