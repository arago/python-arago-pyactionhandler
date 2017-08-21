import time
import gevent
import gevent.queue
from greenlet import GreenletExit
from arago.pyactionhandler.worker import Worker
from arago.pyactionhandler.action import FailedAction
import sys
import logging
import traceback
from weakref import WeakValueDictionary

class WorkerCollection(object):
	def __init__(self, capabilities, parallel_tasks=10, parallel_tasks_per_worker=10, worker_max_idle=300):
		self.logger = logging.getLogger('root')
		self.capabilities=capabilities
		self.parallel_tasks_per_worker=parallel_tasks_per_worker
		self.worker_max_idle=worker_max_idle
		self.workers = WeakValueDictionary()
		self.task_queue=gevent.queue.JoinableQueue(maxsize=parallel_tasks)

	def register_response_queue(self, response_queue):
		self.response_queue=response_queue
		self.logger.info("Registered worker collection for {caps}".format(caps=", ".join(self.capabilities.keys())))

	def get_worker(self, NodeID):
		if NodeID not in self.workers or self.workers[NodeID].shutdown_in_progress:
			self.workers[NodeID] = Worker(
				self, NodeID, self.response_queue,
				self.parallel_tasks_per_worker,
				self.worker_max_idle)
		return self.workers[NodeID]

	def remove_worker(self, worker):
		self.workers = {n: w for n, w in self.workers.items() if w is not worker}

	def shutdown_workers(self):
		self.task_queue.join()
		items = list(self.workers.values())
		for i in items:
			i.shutdown()
		del items

	def handle_requests_per_worker(self):
		self.logger.info("Started forwarding requests")
		while True:
			anum, capability, timeout, params, zmq_info = self.task_queue.get()
			try:
				worker = self.get_worker(params['NodeID'])
				capability = self.capabilities[capability]
				try:
					worker.add_action(capability.action_class(
						anum, params['NodeID'], zmq_info, timeout,
						params, **capability.params))
				except Exception as e:
					self.logger.debug(e)
					dummy_action = FailedAction(
						anum, params['NodeID'], zmq_info, timeout, params)
					dummy_action.statusmsg += "\n" + traceback.format_exc()
					worker.add_action(dummy_action)
			except KeyError:
				self.logger.error("Unknown capability {cap}".format(cap=capability))
			finally:
				del worker, capability
