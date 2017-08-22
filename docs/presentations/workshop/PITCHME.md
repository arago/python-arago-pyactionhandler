---
# HIRO ActionHandlers

+++

1. Overview: ActionHandlers, Capabilities and Applicabilities
2. *External* ActionHandlers: Benefits over the built–in Generic ActionHandler, HIRO Interface
3. PyActionHandler module: Features and Usage
4. Anatomy of an ActionHandler: How to develop a new ActionHandler

---
## Overview
What *is* an ActionHandler?

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
- <span class="fragment">in theory, SQL is a standardized language</span>
- <span class="fragment">*sarcastic laughter*</span>
- <span class="fragment">different dialects can also be handled by “applicability” and KI scope</span>

+++
#### Parameters
- ActionHandlers can specifiy mandatory and optional parameters |
- Optional parameters can have default values |
- Default values can be static or dynamically read from the MARS model |

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

+++

- <span class="fragment">Pick all ActionHandlers that provide the requested Capability</span>
- <span class="fragment">Deselect all ActionHandlers with mandatory parameters not provided by the request</span>
- <span class="fragment">Deselect all ActionHandlers who's Applicability does not match the current MARSNode</span>
- <span class="fragment">Order remaining ActionHandlers by *priority*</span>

+++
### Built–in Actionhandlers

The HIRO Engine has 2 ActionHandlers built–in:

- the Generic ActionHandler |
- the IssueInputDataHandler |

+++
#### The Generic ActionHandler
- Use existing command line tools as ActionHandler
- Configure any number of Capabilities

+++
#### The IssueInputDataHandler
- Interact with cockpit users
- Ask for input, approval etc.

+++

Learn more about the Generic Actionhandler, Capabilities and Applicabilities in section

*Installation & Configuration / Complete your Installation / Generic ActionHandler*

in the HIRO documentation.

https://docs.hiro.arago.co/

---

## External ActionHandlers
The Generic ActionHandler works fine, why deal with external ActionHandlers, anyway?

+++

- “Complexity” or “You don't want to deal with SOAP in a bash oneliner |
- Performance |
- Queuing |
- Keeping state |
- Fallback Handlers |
- Asynchronous ActionHandlers |

+++
### How an external ActionHandler works

- Runs as an external Daemon, possibly on another machine |
- Listens on a ZeroMQ port for messages from the HIRO Engine |
- Messages are encoded as protocol buffers (protobuf) |

+++
#### ZeroMQ
http://zeromq.org

- High-speed message queue |
- Platform / language independed |
- Asynchronous |
- Many usage pattern like request–reply, router–dealer or publish–subscribe |

+++
#### Protocol buffers
https://developers.google.com/protocol-buffers/

- Messages are encoded to a binary “wire format” using a schema |
- The protobuf compiler generates code to read and write these messages |
- Official support for C++, Go, Java, C# and Python |
- Unofficial implementations for many other languages |

+++
##### Example

~~~protobuf
message ActionRequest {
    required string capability = 1;
    required int64 time_out = 2;
    repeated KeyValueMessage params_list = 10;
}

message ActionResponse {
    optional string output = 6;
    optional string error_text = 7;
    optional int32 system_rc = 8;
    required string statusmsg = 3;
    required bool success = 9;
}

service ActionHandler_Service {
    rpc PerformAction(ActionRequest) returns (ActionResponse);
}
~~~
@[1-5](ActionRequest message definition)
@[7-13](ActionResponse message definition)
@[15-17](RPC service definition)

---

## PyActionHandler module features

+++
### Why Python?
- Easy to learn |
- Fast development cycle |
- Huge amount of simple to use 3rd–party modules that cover almost any usecase |

+++
### Features
- Takes care of all communication with the HIRO Engine, including encryption |
- Automatically handles errors, timeouts etc. |
- Built–in concurrency based on gevent |
- Built–in queuing, per ActionHandler and per MARSNode |

---

## Creating an external ActionHandler

+++
### Start with a piece of Python code

~~~python
class CountingRhyme(object):
	def __init__(self):
		self.lines=["Eeny, meeny, miny, moe.",
		            "Catch a tiger by the toe.",
		            "If he hollers, let him go."]
		self._current = 0

	@property
	def current_line(self):
		line = self.lines[self._current]
		self._current = (self._current + 1) % len(self.lines)
		return line

rhyme = CountingRhyme()
print(rhyme.current_line)
~~~
@[2]
@[3-5]
@[6]
@[9-12]
@[14-15]

+++
### Wrap it into a class derived from “Action”

~~~python
class CountingRhymeAction(Action):
	def __init__(self, num, node, zmq_info, timeout, parameters, rhyme):
		super().__init__(num, node, zmq_info, timeout, parameters)
		self.rhyme = rhyme

	def __call__(self):
		self.output = self.rhyme.current_line
		self.error_output = ""
		self.system_rc = 0
		self.statusmsg=""
		self.success = True
~~~
@[1-2]
@[3]
@[4]
@[6]
@[7]
@[8-10]
@[11]

+++
### Define the Capability

~~~python
capabilities = {
	"Rhyme": Capability(CountingRhymeAction, rhyme=rhyme)
}
~~~

+++
### Define a “WorkerCollection”

~~~python
worker_collection = WorkerCollection(
	capabilities,
	parallel_tasks = 10,
	parallel_tasks_per_worker = 3,
	worker_max_idle = 300,
)
~~~
@[2]
@[3]
@[4]
@[5]

+++
### Define the ActionHandler and run it

~~~python
counting_rhyme_handler = SyncHandler(
	worker_collection,
	zmq_url = 'tcp://*:7291'
)

action_handlers = [counting_rhyme_handler]

greenlets=[action_handler.run() for action_handler in action_handlers]
gevent.idle()
gevent.joinall(greenlets)
~~~
@[1]
@[2]
@[3]
@[6]
@[8]
@[9-10]

+++
### Wrap the whole thing into a Daemon

~~~python
class ActionHandlerDaemon(Daemon):
	def run(self):
		rhyme = CountingRhyme()

		...

		gevent.joinall(greenlets)
		sys.exit(0)
~~~
@[1-2]
@[3-7]
@[8]

+++
### Build a small command line interface for the daemon

~~~python
if __name__ == "__main__":
	usage="""\
Usage:
  hiro-counting-rhyme-actionhandler [options] (start|stop|restart)

Options:
  --debug            do not run as daemon and log to stderr
  --pidfile=PIDFILE  Specify pid file [default: /var/run/counting-rhyme.pid]
  -h --help          Show this help screen
"""
	...
~~~
@[3-9]

+++

~~~python
	...

	args=docopt(usage)
	daemon = ActionHandlerDaemon(args['--pidfile'], debug=args['--debug'])

	if args['start']: daemon.start()
	elif args['stop']: daemon.stop()
	elif args['restart']: daemon.restart()
	sys.exit(0)
~~~
@[3]
@[4]
@[6-8]

+++
### Create an init script

An example / template is included with the pyactionhandler module

+++
### Define Capability and Applicability for the HIRO Engine

`/opt/autopilot/conf/external_actionhandlers/capabilities/counting-rhyme.yaml`

~~~yaml
- Applicability:
    - Priotity: 100
      ModelFilter:
        - TrueFilter: {}
  Capability:
    - Name: "Rhyme"
      Description: "Get one or more lines from a counting rhyme"
      Parameter:
        - Name: "Number"
          Description: "The number of lines to get"
          Mandatory: false
~~~
@[1-4]
@[6-7]
@[9-10]
@[11]

+++
### Configure the Engine to use the new ActionHandler

`/opt/autopilot/conf/aae.yaml`

~~~yaml
ActionHandlers:
  ActionHandler:
    - URL: "tcp://127.0.0.1:7291"
      SubscribeURL: ''
      CapabilityYAML: "/opt/autopilot/conf/external_actionhandlers/capabilities/counting-rhyme.yaml"
      RequestTimeout: 60
~~~
@[3]
@[5]

+++
### Encryption
If the ActionHandler does not run on the same machine as the HIRO Engine, the communication should be encrypted.

+++
#### Generating the encryption keys

Server keypair

~~~console
$ /opt/rh/hiro_integration/root/usr/bin/create-zmq-keypair.sh
public  key: J!umAeYQoVi>t]!26B}<x1<H-kXDR{zmX8wl1nz8
private key: yL+!k7f@nevkyt[OD5r5bZ<C6>gZXIIc[?f]U^1L
~~~

Client Keypair

~~~console
$ /opt/rh/hiro_integration/root/usr/bin/create-zmq-keypair.sh
public  key: 881Gr-9IOV0OZ-:.JQE>duS#vMkQJ5wSdkvFnqF5
private key: ^gR.fnp%eh5U5f-G7TnC^ZLXZwk-G$s(G7s9?r((
~~~

Server = ActionHandler

Client = HIRO Engine

+++
#### HIRO Engine configuration

~~~yaml
ActionHandlers:
  ActionHandler:
    - URL: "tcp://127.0.0.1:7291"
      SubscribeURL: ''
      CapabilityYAML: "/opt/autopilot/conf/external_actionhandlers/capabilities/counting-rhyme.yaml"
      RequestTimeout: 60
      client-privatekey: "^gR.fnp%eh5U5f-G7TnC^ZLXZwk-G$s(G7s9?r(("
      client-publickey: "881Gr-9IOV0OZ-:.JQE>duS#vMkQJ5wSdkvFnqF5"
      server-publickey: "J!umAeYQoVi>t]!26B}<x1<H-kXDR{zmX8wl1nz8"
~~~
@[7-8]
@[9]

+++
#### ActionHandler

~~~python
server_public_key = b'J!umAeYQoVi>t]!26B}<x1<H-kXDR{zmX8wl1nz8'
server_private_key = b'yL+!k7f@nevkyt[OD5r5bZ<C6>gZXIIc[?f]U^1L'

counting_rhyme_handler = SyncHandler(
	worker_collection,
	zmq_url = 'tcp://*:7291'
	auth = (server_public_key, server_private_key)
)
~~~
@[1-2]
@[7]

+++
### Packaging
- CentOS / RHEL 6.x by default include only a very old Python (2.6.6) |
- The pyactionhandler module requires Python 3.2 or newer |
- Python 3.4.x and 3.5.x are available as “Software Collection” that can be installed in parallel |
- Unfortunately, this makes packaging programs that depend on it bit more difficult |

---
## Learn more

+++
### HIRO & ActionHandlers

https://docs.hiro.arago.co

https://github.com/arago/python-arago-pyactionhandler

https://github.com/arago/hiro-winrm-actionhandler

https://github.com/arago/hiro-snow-actionhandler

https://repository.arago.de/hiro-contrib/

+++
### 3rd–party components

http://zeromq.org

https://developers.google.com/protocol-buffers/

http://www.gevent.org

http://docopt.org

### Presentation

This presentation is available at http://bit.ly/actionhandler-workshop

