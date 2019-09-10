#!/usr/bin/env python
import os
if os.environ.get('USER','') == 'vagrant':
    del os.link

import distutils.core

distutils.core.setup(
	name = "python-arago-actionhandler",
	version = "0.1",
	author = "Marcus Klemm",
	author_email = "mklemm@arago.de",
	description = ("HIRO 6.0 REST actionhandler interface"),
	license = "MIT",
	url = "http://www.arago.de",
	long_description="HIRO 6.0 REST actionhandler interface",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
	],
	packages=['arago.actionhandler.servers.rest',
	],
	install_requires=['gevent', 'falcon', 'fastjsonschema', 'gevent-tiny-actorsystem']
)
