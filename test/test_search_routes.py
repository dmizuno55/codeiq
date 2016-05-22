import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_routes import Point
from search_routes import Track
from search_routes import Explorer

explorer = Explorer(5, 4)
explorer.go(Point.get_point(0, 0))

explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
explorer.go(explorer.get_available_points()[0])
print(explorer)

explorer.back()
print(explorer)
