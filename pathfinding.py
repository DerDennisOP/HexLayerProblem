import dijkstra3d
import numpy as np

field = np.ones((12, 12, 12, 12), dtype=np.int32)
source = (0,0,0,0)
target = (11, 11, 11, 11)

path = dijkstra3d.dijkstra(field, source, target, bidirectional=True)
print(path)