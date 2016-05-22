import cProfile
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_routes import Point
from search_routes import Track
from search_routes import Explorer
from search_routes import explore
from search_routes import search_routes

def run():
    #search_routes(5, 4, 21)

    explorer = Explorer(5, 4)
    explorer.go(Point.get_point(0, 0))

    explore(explorer, 21)

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.runcall(run)
    profiler.print_stats()
