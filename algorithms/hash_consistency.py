"""Code from http://www.jianshu.com/p/e8fb89bb3a61."""
# -*- coding: utf-8 -*-
from zlib import crc32
# import memcache


class HashConsistency(object):

	def __init__(self, nodes=None, replicas=5):
		# 虚拟节点和真实节点对应的关系
		self.nodes_map = []
		# 真实节点与虚拟节点的字典映射
		self.nodes_replicas = {}
		# 真实节点
		self.nodes = nodes
		self.replicas = replicas

		if self.nodes:
			for node in self.nodes:
				self._add_nodes_map(node)
			self._sort_nodes()


	def get_node(self, key):
		"""根据key值的hansh值， 返回对应的节点
		算法是：返回最早比key_hash大的节点
		"""
		key_hash = abs(crc32(key))
		for node in self.nodes_map:
			if key_hash > node[0]:
				continue
			return node
		return None

	def add_node(self, node):
		"""添加节点."""
		self._add_nodes_map(node)
		self._sort_nodes()

	def remove_node(self, node):
		"""删除节点."""
		if node not in self.nodes_replicas.keys():
			pass
		discard_rep_nodes = self.nodes_replicas[node]
		self.nodes_map = filter(lambda x: x[0] not in discard_rep_nodes, self.nodes_map)

	def _add_nodes_map(self, node):
		"""增加虚拟节点到nodes_map列表."""
		nodes_reps = []
		for i in xrange(self.replicas):
			rep_nodes = '%s_%s' % (node, i)
			node_hash = abs(crc32(rep_nodes))
			self.nodes_map.append((node_hash, node))
			nodes_reps.append(node_hash)
		# 真实节点与虚拟节点的字典映射
		self.nodes_replicas[node] = nodes_reps

	def _sort_nodes(self):
		# 按顺序排列虚拟节点
		self.nodes_map = sorted(self.nodes_map, key=lambda x:x[0])


memcache_server = {
	'127.0.0.1:7001',
	'127.0.0.1:7002',
	'127.0.0.1:7003',
	'127.0.0.1:7004'
}

hs = HashConsistency(memcache_server)

for k in hs.nodes_map:
	print k

mc_server_dict = {}

for ms in memcache_server:
	# mc = memcache.Client([ms], debug=0)
	mc = 'memcahe.Client(%s)' % ms
	mc_server_dict[ms] = mc

# 循环10给memcache添加key, 这里使用了一致性hash, 那么key将会根据hash值
# 落点到对应的虚拟节点上
for i in xrange(10):
	key = 'key_%s' %i
	print key
	server = hs.get_node(key)[1]
	mc = mc_server_dict[server]
	mc = mc + '---' + key + '----' + str(i)
	print 'Server: %s' % server
	print mc
