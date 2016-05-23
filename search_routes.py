import pprint
import threading

pp = pprint.PrettyPrinter(indent=2, width=100)

class Point:
    points = {}

    @classmethod
    def get_point(cls, x, y):
        if not x in cls.points:
            cls.points[x] = {}

        if not y in cls.points[x]:
            cls.points[x][y] = Point(x, y)

        return cls.points[x][y]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_path(self, other):
        return frozenset((self, other))

    def __repr__(self):
        return str(self.__dict__)

class Track:
    def __init__(self):
        self.points= []
        self.corner_count = 0

    def is_already_passed(self, target_point):
        if not target_point in self.points:
            return False

        last_point = self.points[-1]

        before = None
        for current in self.points:
            if before:
                if last_point == before and target_point == current:
                    return True

                if target_point == before and last_point == current:
                    return True

            before = current

        return False

    def can_go_to(self, point):
        if self.points:
            last_point = self.points[-1]

            if last_point == point:
                return False

            if last_point.x != point.x and last_point.y != point.y:
                return False

            if self.is_already_passed(point):
                return False

        return True

    def is_corner(self, point):
        if len(self.points) < 2:
            return False

        b1 = self.points[-1]
        b2 = self.points[-2]
        if b1.x == b2.x:
            return b2.x != point.x
        else:
            return b2.y != point.y

    def go(self, point):
        # if not self.can_go_to(point):
        #     raise Exception('can not go to')

        if self.is_corner(point):
            self.corner_count = self.corner_count + 1

        self.points.append(point)

    def back(self):
        last_point = self.points.pop()
        if self.is_corner(last_point):
            self.corner_count = self.corner_count - 1

        return last_point

    def dump(self):
        return self.points[:]

    def clone(self):
        clone = Track()
        clone.points = self.points[:]
        clone.corner_count = self.corner_count

        return clone

    def __repr__(self):
        return str(self.__dict__)

class Explorer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.goal = Point.get_point(x - 1, y - 1)
        self.track = Track()
        self.markers = []
        self.snapshots = []

    def get_around_points(self, point):
        points = []
        over_x = point.x + 1
        under_x = point.x - 1
        over_y = point.y + 1
        under_y = point.y - 1

        if over_x < self.x:
            points.append(Point.get_point(over_x, point.y))

        if over_y < self.y:
            points.append(Point.get_point(point.x, over_y))

        if under_x >= 0:
            points.append(Point.get_point(under_x, point.y))

        if under_y >= 0:
            points.append(Point.get_point(point.x, under_y))

        return points

    def get_available_points_at(self, point):
        track = self.track
        around_points = self.get_around_points(point)

        return [p for p in around_points if track.can_go_to(p)]

    def get_available_points(self):
        if not self.markers:
            return []

        marker = self.markers[-1]
        return marker['choices']

    def go(self, point):
        track = self.track

        if self.is_reached():
            raise Exception('already reach goal.')

        if self.markers:
            marker = self.markers[-1]
            if not point in marker['choices']:
                raise Exception('not found in choices.\n' + str(self) + '\n' + str(point))

            marker['choices'].remove(point)

        track.go(point)

        new_marker = {'point': point, 'choices': self.get_available_points_at(point)}

        self.markers.append(new_marker)


    def back(self):
        markers = self.markers
        last_marker = markers.pop()

        track = self.track
        last_point = track.back()

        # print('back()', last_marker, last_point, track.corner_count)

    def is_reached(self):
        track = self.track
        if not track.points:
            return False

        return self.goal == track.points[-1]

    def save_track(self):
        track = self.track
        self.snapshots.append(track.dump())

    def fork(self):
        if not self.markers:
            return None

        last_marker = self.markers[-1]
        if not last_marker['choices']:
            return None

        clone = Explorer(self.x, self.y)
        clone.track = self.track.clone()

        start_point = last_marker['choices'][0]
        last_marker['choices'].remove(start_point)

        clone.go(start_point)

        return clone

    def __repr__(self):
        return 'track: %(track)s\nmarkers: %(markers)s' % {'track': pp.pformat(self.track), 'markers': pp.pformat(self.markers)}


def is_over_count(explorer, count):
    track = explorer.track
    if track.corner_count > count:
        return True

    if track.corner_count == count:
        last_point = track.points[-1]
        goal = explorer.goal
        if last_point.x != goal.x and last_point.y != goal.y:
            return True

    return False


def is_dead_end(explorer):
    if not explorer.markers:
        return False
    
    marker = explorer.markers[-1]
    
    if not marker['choices']:
        return True
    else:
        return False

def is_completed(explorer):
    if not explorer.markers:
        return True

    return False

def is_closed_y_line(explorer, target):
    track = explorer.track
    track_points = track.points

    closed = set()
    closed.add(target.x)

    before = None
    for current in track_points:
        if before and before.x == current.x and (before.y > target.y or current.y > target.y):
            closed.add(current.x)

        before = current

    if len(closed) == explorer.x:
        print(track)

    return closed.issuperset(set(range(explorer.x)))

def is_closed_x_line(explorer, target):
    track = explorer.track
    track_points = track.points

    closed = set()
    closed.add(target.y)

    before = None
    for current in track_points:
        if before and before.y == current.y and (before.x > target.x or current.x > target.x):
            closed.add(current.y)

        before = current

    if len(closed) == explorer.y:
        print(track)
    return closed.issuperset(set(range(explorer.y)))

def prune(explorer):
    markers = explorer.markers
    if not markers:
        return

    track = explorer.track
    track_points = track.points
    if not track_points:
        return

    marker = markers[-1]
    last_point = track_points[-1]

    prune_list = []
    for point in explorer.get_available_points():
        if last_point.y > point.y and is_closed_y_line(explorer, point):
            prune_list.append(point)
            continue

        if last_point.x > point.x and is_closed_x_line(explorer, point):
            prune_list.append(point)
            continue

    for point in prune_list:
        marker['choices'].remove(point)

def explore(explorer, count):
    while not is_completed(explorer):
        prune(explorer)

        points = explorer.get_available_points()
        if points:
            explorer.go(points[0])

        if explorer.is_reached():
            if explorer.track.corner_count == count:
                explorer.save_track()
            
            # print('is_reached()')
            explorer.back()

        if is_over_count(explorer, count):
            # print('is_over_count()')
            explorer.back()

        if is_dead_end(explorer):
            # print('is_dead_end()')
            while is_dead_end(explorer):
                explorer.back()

    return explorer

def fork(explorer, depth):
    child_explorers = []
    for point in explorer.get_available_points()[:]:
        child = explorer.fork()
        child_explorers.append(child)
        if depth < 1:
            child_explorers.extend(fork(child, depth - 1))

    return child_explorers

def search_routes(size_x, size_y, count):
    explorer = Explorer(size_x, size_y)

    explorer.go(Point.get_point(0, 0))

    explorers = [explorer]
    explorers.extend(fork(explorer, 3))

    processes = [threading.Thread(group=None, target=explore, args=(ex, count)) for ex in explorers]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    result = 0
    for ex in explorers:
        # print(len(ex.snapshots), ex.go_count)
        result = result + len(ex.snapshots)
    print(result)

if __name__ == '__main__':
    SIZE_X = 5
    SIZE_Y = 4

    try:
        while True:
            count = int(input())
            search_routes(SIZE_X, SIZE_Y, count)
    except EOFError:
        pass

