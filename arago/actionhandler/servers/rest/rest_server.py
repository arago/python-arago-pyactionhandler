from arago.actors import Actor, Source
import falcon
import fastjsonschema
import gevent, gevent.pywsgi
import logging
#from loguru import logger
import weakref

from urllib.parse import urlparse, urlunparse
from uuid import uuid4

#from arago.actors.symbols import OK, FAIL

def schema_validation(req, resp, resource, *args, **kwargs):
	logger = logging.getLogger('root')
	schema = kwargs["schema"]
	rtype = "Request" if schema == "req_schema" else "Response"
	l = locals()
	obj = l["req"] if schema == "req_schema" else l["resp"]
	try:
		val = resource._validators[schema]
		val(obj.media)
		logger.trace("{rtype} was successfully validated against schema.".format(rtype=rtype))
	except fastjsonschema.JsonSchemaException:
		logger.warn("Request could not be validated against schema.")
		raise falcon.HTTPBadRequest(description="Request could not be validated against schema.")
	except KeyError:
		logger.debug("No schema for {rtype} given, skipping validation.".format(rtype=rtype))

class RestServer(Source):
	def __init__(self, endpoint, app, certfile=None, keyfile=None, *args, **kwargs):
		self._logger = logging.getLogger('root')
		self._endpoint=urlparse(endpoint)
		if certfile and keyfile:
			ssl_args = {'certfile': certfile, 'keyfile': keyfile}
		else:
			ssl_args = {}
		server = gevent.pywsgi.WSGIServer(
			(self._endpoint.hostname, self._endpoint.port),
			app,
			log=gevent.pywsgi.LoggingLogAdapter(self._logger, level=self._logger.VERBOSE),
			error_log=self._logger,
			**ssl_args)
		super().__init__(server, *args, **kwargs)

class HIROEngineSyncRESTInterface(RestServer):
	def __init__(self, handler, endpoint, req_schema=None, resp_schema=None, *args, **kwargs):
		self._app = falcon.API()
		self._routes = {
			'/request': HIROEngineSyncRESTInterface.Endpoint(handler, req_schema, resp_schema,
			                                                 actor=weakref.proxy(self))
		}
		[self._app.add_route(route, handler) for route, handler in self._routes.items()]
		super().__init__(endpoint, self._app, *args, **kwargs)

	class Endpoint(object):
		def __init__(self, handler, req_schema=None, resp_schema=None, actor=None):
			self._actor = actor
			self._logger = logging.getLogger('root')
			self._handler = handler
			l = locals()
			self._validators = {
				name: fastjsonschema.compile(l[name])
				for name in ["req_schema", "resp_schema"]
				if l[name]
			}

		@falcon.before(schema_validation, schema="req_schema")
		@falcon.after(schema_validation, schema="resp_schema")
		def on_post(self, req, resp):
			try:
				result = self._handler.wait_for("action_request", req.media, sender=self._actor)
				resp.media = {
					"status": "done",
					"result": result
				}
				resp.status = falcon.HTTP_200
			except Exception as e:
				#raise falcon.HTTPInternalServerError(description=str(e))
				resp.status = falcon.HTTP_200
				resp.media = {
					'status': 'done',
					'result': {'exec': str(e)}
				}
