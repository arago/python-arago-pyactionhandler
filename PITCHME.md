---
# HIRO ActionHandlers

+++
```python
class CountingRhyme(object):
	def __init__(self):
		self.lines=[
			"Eeny, meeny, miny, moe.",
			"Catch a tiger by the toe.",
			"If he hollers, let him go."
		]
		self._current = 0

	@property
	def current_line(self):
		line = self.lines[self._current]
		self._current = (self._current + 1) % len(self.lines) # increase counter, loop at the end
		return line

rhyme = CountingRhyme()
print(rhyme.current_line)
```
@[1](class creation)

---
## Overview
---
## External ActionHandlers
---
## PyActionHandler module features & usage
---
## Creating an external ActionHandler
