# coding: iso-8859-1

import sys
import math
import random

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
				print("cache =",self.cache)	
				return False # Cache Hit
		return True # Cache Miss

	def update(self, obj): # Add or replace the request content
		self.cache[self.tail] = obj;
		self.tail = (self.tail + 1) % len(self.cache)
		if self.size < len(self.cache):
			self.size += 1
		print("cache =",self.cache)	

	def printLog(self):
		print("Total Requests: " + str(self.count) + ", Total Cache Hit: " + str(self.cacheHit) + ", Total Cache Miss: " + str(self.count - self.cacheHit) + \
				", Cache Hit Ratio: " + str(round(self.cacheHit/self.count,2)) + ", Cache Miss Ratio: " + str( round( (self.count - self.cacheHit)/self.count, 2 ) ) )

class LRU:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize
		self.age = [0] * cacheSize
		self.count = 0
		self.cacheHit = 0

	def search(self, obj):
		self.count += 1
		for i in range(self.size):
			if obj == self.cache[i]:
				self.cacheHit += 1
				self.age[i] = self.count
				
				print("cache =",self.cache, ", age =", self.age )
				
				return False
		return True

	def update(self, obj):

		if self.size < len(self.cache): # while the cache is not full, add the new item at the end
			self.cache[self.size] = obj
			self.age[self.size] = self.count
			
			print("cache =",self.cache, ", age =", self.age )
			self.size += 1
		else: # if the cache is full, replace items through the LRU policy 
			ageMin, ageMinPos = self.age[0], 0 
			for i in range(1, self.size):
				if self.age[i] < ageMin:
					ageMin = self.age[i]
					ageMinPos = i

			self.cache[ageMinPos] = obj
			self.age[ageMinPos] = self.count
		
			print("cache =",self.cache, ", age =", self.age )
			
	def printLog(self):
		print("Total Requests: " + str(self.count) + ", Total Cache Hit: " + str(self.cacheHit) + ", Total Cache Miss: " + str(self.count - self.cacheHit) + \
				", Cache Hit Ratio: " + str(round(self.cacheHit/self.count,2)) + ", Cache Miss Ratio: " + str( round( (self.count - self.cacheHit)/self.count, 2 ) ) )

class LFU:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize
		self.access = [0] * cacheSize
		self.count = 0
		self.cacheHit = 0

	def search(self, obj):
		self.count += 1
		for i in range(self.size):
			if obj == self.cache[i]:
				self.cacheHit += 1
				self.access[i] += 1
				print("cache =",self.cache, ", access =", self.access )
				return False
		return True

	def update(self, obj):

		if self.size < len(self.cache): # while the cache is not full, add the new item at the end
			self.cache[self.size] = obj
			self.access[self.size] = 1
			print("cache =",self.cache, ", access =", self.access )
			self.size += 1
		else: # if the cache is full, replace items through the LFU policy 
			accessMin, accessMinPos = self.access[0], 0 
			for i in range(1, self.size):
				if self.access[i] < accessMin:
					accessMin = self.access[i]
					accessMinPos = i

			self.cache[accessMinPos] = obj
			self.access[accessMinPos] = 1

			print("cache =",self.cache, ", access =", self.access )

	def printLog(self):
		print("Total Requests: " + str(self.count) + ", Total Cache Hit: " + str(self.cacheHit) + ", Total Cache Miss: " + str(self.count - self.cacheHit) + \
				", Cache Hit Ratio: " + str(round(self.cacheHit/self.count,2)) + ", Cache Miss Ratio: " + str( round( (self.count - self.cacheHit)/self.count, 2 ) ) )

class Random:

	def __init__(self, cacheSize):
		self.size = 0
		self.cache = [None] * cacheSize
		self.count = 0
		self.cacheHit = 0

	def search(self, obj):
		self.count += 1
		for i in range(self.size):
			if obj == self.cache[i]:
				self.cacheHit += 1
				print("cache =",self.cache )
				return False # Cache Hit
		return True # Cache Miss

	def update(self, obj):

		if self.size < len(self.cache): # while the cache is not full, add the new item at the end
			self.cache[self.size] = obj
			print("cache =",self.cache )
			self.size += 1
		else:
			rVal = random.randint(0, len(self.cache)-1 )
			self.cache[rVal] = obj
			print("cache =",self.cache )

	def printLog(self):
		print("Total Requests: " + str(self.count) + ", Total Cache Hit: " + str(self.cacheHit) + ", Total Cache Miss: " + str(self.count - self.cacheHit) + \
				", Cache Hit Ratio: " + str(round(self.cacheHit/self.count,2)) + ", Cache Miss Ratio: " + str( round( (self.count - self.cacheHit)/self.count, 2 ) ) )

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
