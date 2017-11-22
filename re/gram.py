from parsimonious.grammar import Grammar
grammar = Grammar(
	"""
	bold_text  = bold_open text bold_close
	text       = ~"[A-Z 0-9]*"i
	bold_open  = "(("
	bold_close = "))"
	""")

print grammar.parse('((bold stuff))')