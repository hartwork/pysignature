# Copyright (C) 2013 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function


_HAS_STAR_ARGS = 0b100
_HAS_DOUBLE_STAR_ARGS = 0b1000


def _format_default(value):
	if isinstance(value, basestring):
		value = value.replace('\\', '\\\\')
		value = value.replace("'", "\\'")
		return "'%s'" % value

	return value


def signature(f, format_default=_format_default):
	args = list()
	regular_arg_count = f.func_code.co_argcount
	defaults_offset = regular_arg_count - len(f.func_defaults or list())
	for i in range(regular_arg_count):
		if i >= defaults_offset:
			key = f.func_code.co_varnames[i]
			default = format_default(f.func_defaults[i - defaults_offset])
			args.append('%s=%s' % (key, default))
		else:
			args.append(f.func_code.co_varnames[i])

	if f.func_code.co_flags & _HAS_STAR_ARGS:
		if f.func_code.co_flags & _HAS_DOUBLE_STAR_ARGS:
			args.append('*%s' % f.func_code.co_varnames[regular_arg_count])
			args.append('**%s' % f.func_code.co_varnames[regular_arg_count + 1])
		else:
			args.append('*%s' % f.func_code.co_varnames[regular_arg_count])
	elif f.func_code.co_flags & _HAS_DOUBLE_STAR_ARGS:
		args.append('**%s' % f.func_code.co_varnames[regular_arg_count])

	return '%s(%s)' % (f.func_name, ', '.join(args))


if __name__ == '__main__':
	def f1(one, two="22", three=33, four=object()):
		a = 14

	def f2(one, two):
		a = 14

	def f3(one, *args):
		a = 14

	def f4(one, **kvargs):
		a = 14

	def f5(one, *args, **kvargs):
		a = 14

	for f in (f1, f2, f3, f4, f5):
		print(f.__name__)
		print('  func_code.co_argcount =', f.func_code.co_argcount)
		print('  func_code.co_varnames =', f.func_code.co_varnames)
		print('  func_code.co_flags =', bin(f.func_code.co_flags))
		print('  func_defaults =', f.func_defaults)
		print('  -> %s' % signature(f))
		print()
