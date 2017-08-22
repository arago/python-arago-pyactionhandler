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
- <span class="fragment">`ExecuteCommand`</span>
- <span class="fragment">`ExecuteRemoteCommand`</span>
- <span class="fragment">`ExecuteShellCommand`</span>

+++
#### Over–specific names:
- <span class="fragment">`ExecuteCommandViaJumpserver`: What if you don't have a jump server?</span>
- <span class="fragment">`ExecuteCommandSSH`: What if you want the commands to be executed via netsh?</span>
- <span class="fragment">`OpenSNOWTicket`: What if you're using HPSM?</span>

+++
#### Just bad names:
- <span class="fragment">`RunSoln`: ???</span>

+++
#### Quiz
Which of the following examples are bad names and why?

+++
##### `ExecuteRemoteCommand`
- <span class="fragment">Nothing particulary bad about the name</span>
- <span class="fragment">For historic reasons, this is already covered by `ExecuteCommand`</span>

+++
##### `ExecuteCommandOnJumpserver`
- <span class="fragment">debateable</span>
- <span class="fragment">does not describe the *how*, but the *what*</span>
- <span class="fragment">KnowledgeItems that use this capability will probably not be of any use in environments lacking a jumpserver, anyway</span>

+++
##### `QueryMSSQL`
- <span class="fragment">debateable (again)</span>
- <span class="fragment">in theory, SQL is a standardize language</span>
- <span class="fragment">different dialects can also be handled by “applicability” and KI scope</span>

+++
### Applicabilities …
- <span class="fragment">describe a subset of the MARS model where an ActionHandler can be used</span>
- <span class="fragment">same principle as the `On` section in a Knowledge Item</span>

---

## External ActionHandlers

---

## PyActionHandler module features & usage

---

## Creating an external ActionHandler
