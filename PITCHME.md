---
# HIRO ActionHandlers
---
## Overview
What *is* and ActionHandler?

+++
### ActionHandlers …
- <span class="fragment">are the *hands* of the HIRO Engine</span>
- <span class="fragment">can execute commands or call external systems</span>
- <span class="fragment">implement one or multiple “capabilities”</span>
- <span class="fragment">are limited to a subset of the MARS model by their “applicability”</span>

+++
### Capabilities …
- <span class="fragment">are “identifiers”, i.e. strings</span>
- <span class="fragment">describe *what* an ActionHandler can do</span>
- <span class="fragment">should *not* describe how an ActionHandler operates</span>
- <span class="fragment">are “hardcoded” in the Knowledge Items</span>

+++
#### The problem:
Bad names prevent KI reusability

+++
#### Different names for the same thing:
- `ExecuteCommand` |
- `ExecuteRemoteCommand` |
- `ExecuteShellCommand` |

+++
#### Over–specific names:
- `ExecuteCommandViaJumpserver`: What if you don't have a jump server? |
- `ExecuteCommandSSH`: What if you want the commands to be executed via netsh? |
- `OpenSNOWTicket`: What if you're using HPSM? |

+++
#### Just bad names:
-`RunSoln`: ??? |

+++
#### Quiz
Which of the following examples are bad names and why?

+++

- `ExecuteRemoteCommand`
- Nothing particulary bad about the name |
- For historic reasons, this is already covered by `ExecuteCommand` |

+++

- `ExecuteCommandOnJumpserver`
- debateable |
- does not describe the *how*, but the *what* |
- KnowledgeItems that use this capability will probably not be of any use in environments lacking a jumpserver, anyway |

+++

- `QueryMSSQL`
- debateable (again) |
- in theory, SQL is a standardize language |
- different dialects can also be handled by “applicability” and KI scope |

+++
### Applicabilities …
- describe a subset of the MARS model where an ActionHandler can be used |
- same principle as the `On` section in a Knowledge Item

---

## External ActionHandlers

---

## PyActionHandler module features & usage

---

## Creating an external ActionHandler
