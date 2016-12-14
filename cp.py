import os
import sys
import os.path
for root, dirs, files in os.walk(sys.argv[1]):
	for name in files:
		if not os.path.exists(sys.argv[2]+root[len(sys.argv[1]):len(root)]) :
			#print "create "+ sys.argv[2]+root[len(sys.argv[1]):len(root)]
			os.makedirs(sys.argv[2]+root[len(sys.argv[1]):len(root)])
		source = open(root+'/'+name, "r")
		target = open(sys.argv[2]+(root+'/'+name)[len(sys.argv[1]):len(root+'/'+name)], "w+")
		while True: 
			context  = source.read(100)
			if not context:
				source.close()
				target.close()
				break
			target.write(context)


		print (root+'/'+name)
		# print root + '/' + name
