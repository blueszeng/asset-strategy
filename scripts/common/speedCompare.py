import time
import math
start=time.time()
for i in range(0,100000):
	math.sqrt(10000)
print('十万次开根号花时间:{0}'.format(time.time()-start))

start=time.time()
for j in range(0,100000):
	10*10
print('十万次乘法画时间:{0}'.format(time.time()-start))

start=time.time()
for j in range(0,100000):
	math.acos(-0.75)
print('十万次acos画时间:{0}'.format(time.time()-start))