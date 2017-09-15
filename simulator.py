# coding: iso-8859-1

import sys

class FIFO:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize
		self.tail = 0
		self.count = 0
		self.cacheHit = 0

	def search(self, obj): 
		self.count += 1
		for i in range(self.size):
			if obj == self.cache[i]:
				self.cacheHit += 1
				#print(obj,"Cache hit")
				return False
		return True

	def update(self, obj):
		self.cache[self.tail] = obj;
		self.tail = (self.tail + 1) % len(self.cache)
		if self.size < len(self.cache):
			self.size += 1
		print(self.cache)		

	def printLog(self):
		print("Total Requests: " + str(self.count) + ", Total Cache Hit: " + str(self.cacheHit) + ", Total Cache Miss: " + str(self.count - self.cacheHit) + \
				", Cache Hit Ratio: " + str(self.cacheHit/self.count) + ", Cache Miss Ratio: " + str((self.count - self.cacheHit)/self.count) )

class LRU:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize

	def search(self, obj):
		pass
	def update(self):
		pass

class LFU:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize

	def search(self, obj):
		pass
	def update(self):
		pass

class Random:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize

	def search(self, obj):
		pass
	def update(self):
		pass

def main(argv):

	requestFilePath = argv[1]
	cacheSize = int(argv[2])
	replacementPolicy = argv[3]

	Manager = []

	if replacementPolicy.lower() == "fifo":
		Manager = FIFO(cacheSize);
	elif replacementPolicy.lower() == "lru":
		Manager = LRU(cacheSize);
	elif replacementPolicy.lower() == "lfu":
		Manager = LFU(cacheSize);
	elif replacementPolicy.lower() == "random":
		Manager = Random(cacheSize);
	else:
		print("The replacement policy was not chosen correctly!")
		return

	requestFile = open(requestFilePath, "r")

	for request in requestFile:
		request = request.strip()
		cacheMiss = Manager.search(request)

		if cacheMiss:
			Manager.update(request)

	Manager.printLog()

	requestFile.close()

if __name__ == "__main__":
    main(sys.argv)
