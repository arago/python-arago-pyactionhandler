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
##### `Execute_Remote_Command`
- <span class="fragment">Nothing particulary bad about the name</span>
- <span class="fragment">For historic reasons, this is already covered by `ExecuteCommand`</span>

+++
##### `Execute_Command_On_Jumpserver`
- <span class="fragment">debateable</span>
- <span class="fragment">does not describe the *how*, but the *what*</span>
- <span class="fragment">KnowledgeItems may not be of any use in environments lacking a jumpserver, anyway</span>

+++
##### `Query_MS_SQL`
- <span class="fragment">debateable (again)</span>
- <span class="fragment">in theory, SQL is a standardize language</span>
- <span class="fragment">*sarcastic laughter*</span>
- <span class="fragment">different dialects can also be handled by “applicability” and KI scope</span>

+++
#### Parameters
- ActionHandlers can specifiy mandatory and optional parameters
- Optional parameters can have default values
- Default values can be static or dynamically read from the MARS model

+++

~~~yaml
- Applicability:
  …
  Capability:
    - Name: ExecuteCommand
        Description: "execute command on remote host"
        Parameter:
          - Name: Command
              Description: "command to execute"
              Mandatory: true
          - Name: User
              Description: "target user"
              Default: root
          - Name: Hostname
              Description: "host to execute command on"
              Default: ${FQDN}
~~~
@[4](Capability Name)
@[5](Description)
@[7-9](Mandatory parameter)
@[10-12](Static default value)
@[13-15](Dynamic default value)

+++
### Applicabilities …
- <span class="fragment">describe a subset of the MARS model where an ActionHandler can be used</span>
- <span class="fragment">same principle as the `On` section in a Knowledge Item</span>

+++

![KnowledgeItem On section](docs/presentations/assets/screenshot_kie_on.png)

+++

~~~xml
<KI xmlns="https://graphit.co/schemas/v2/KiSchema">
    <Title/>
    <Description/>
    <On>
        <Description>Windows Server 2012 or newer</Description>
        <Var Mode="string" Name="MachineClass" Value="Windows" />
        <Var Mode="string" Name="OSName" Value="Windows Server" />
        <Var Mode="ge" Name="OSMajorVersion" Value="6" />
        <Var Mode="ge" Name="OSMinorVersion" Value="2" />
    </On>
</KI>
~~~
@[6](MachineClass == "Windows")
@[7](OSName == "Windows Server")
@[8](OSMajorVersion >= 6)

+++

~~~yaml
- Applicability:
    - Priority: 50
        ModelFilter:
          - Var:
              Name: MachineClass
              Mode: string
              Value: Windows
          - Var:
              Name: OSName
              Mode: string
              Value: Windows Server
          - Var:
              Name: OSMajorVersion
              Mode: ge
              Value: 6
          - Var:
              Name: OSMinorVersion
              Mode: ge
              Value: 2
~~~
@[4-7](MachineClass == "Windows")
@[8-11](OSName == "Windows Server")
@[12-15](OSMajorVersion >= 6)

+++
### How the HIRO Engine selects an ActionHandler
There can be multiple ActionHandlers that implement the same Capability.

- <span class="fragment">Pick all ActionHandlers that provide the requested Capability</span>
- <span class="fragment">Deselect all ActionHandlers with mandatory parameters not provided by the request</span>
- <span class="fragment">Deselect all ActionHandlers who's Applicability does not match the current MARSNode</span>
- <span class="fragment">ActionHandlers without an Applicability match all MARSNodes</span>
- <span class="fragment">Order remaining ActionHandlers by *priority*</span>

+++

Learn more about Capabilities and Applicabilities in section *Installation & Configuration / Complete your Installation / Generic ActionHandler* in the HIRO documentation.

http://docs.hiro.arago.co

---

## External ActionHandlers

---

## PyActionHandler module features & usage

---

## Creating an external ActionHandler
