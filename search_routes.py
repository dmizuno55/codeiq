from enum import Enum

class Point:
    points = [[]]
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def get_point(cls, x, y):
        if not cls.points[x][y]:
            cls.points[x][y] = Point(x, y)
        return cls.points[x][y]

    def __repr__(self):
        return '{{x: {0}, y: {1} }}'.format(self.x, self.y)

class Route:
    def __init__(point):
        self.pathes= list(point)
        self.corner_count = 0

    @staticmethod
    def calculate_path(p1, p2):
        if p1.x == p2.x:
            return (p1.x, p1.y + p2.y)
        else:
            return (p1.x + p2.x, p1.y)

    def is_already_passed(self, expected_path)
        before = None
        for current in self.pathes:
            if before:
                path = calculate_path(before, current)
                if path == expected_path:
                    return True

            before = current

        return False


    def can_go_to(self, point):
        last_point = self.pathes[-1]

        if last_point == point:
            return False

        if last_point.x != point.x and last_point.y != point.y:
            return False

        expected_path = calculate_path(last_point, point)

        if self.is_already_passed(expected_path):
            return False

        return True

    def is_corner(self, point):
        b1, b2 = self.pathes[-2:]
        if b1.x == b2.x:
            return b2.x != point.x
        else:
            return b2.y != point.y

    def go_to_x(self, x):
        last_point = self.pathes[-1]
        next_point = Point.get_point(x, last_point.y)
        if not self.can_go_to(next_point):
            raise Exception('can not go to')

        if self.is_corner(next_point):
            self.corner_count = self.corner_count + 1

        self.pathes.append(next_point)

    def go_to_y(self, y):
        last_point = self.pathes[-1]
        next_point = Point.get_point(last_paint.x, y)
        if not self.can_go_to(next_point):
            raise Exception('can not go to')

        if self.is_corner(next_point):
            self.corner_count = self.corner_count + 1

        self.pathes.append(next_point)

    def go_back(self):
        last_point = self.pathes.pop()
        if self.is_corner(last_point):
            self.corner_count = self.corner_count - 1

    def __repr__(self):
        return str(self.pathes)

def search_next_pathes(base, size_x, size_y, history):
    pathes = []
    
    if base.x == size_x - 1 and base.y == size_y - 1:
        return pathes

    if base.direction != Path.Direction.x:
        pathes.extend(search_x_pathes(base, size_x, history))
        
    if base.direction != Path.Direction.y:
        pathes.extend(search_y_pathes(base, size_y, history))
    
    return pathes

def search_x_pathes(base, size_x, history):
    pathes = []
    for x in range(1, size_x):
        if not base.can_go_to(x, base.y, Path.Direction.x):
            continue
            
        next_path = base.go_to_x(x)
        if can_pass_through(next_path, history):
            pathes.append(next_path)

    return pathes

def search_y_pathes(base, size_y, history):
    pathes = []
    for y in range(1, size_y):
        if not base.can_go_to(base.x, y, Path.Direction.y):
            continue
            
        next_path = base.go_to_y(y)
        if can_pass_through(next_path, history):
            pathes.append(next_path)

    return pathes

def can_pass_through(path, history):
    if path in history:
        return False
    return True

def search_routes(point, size_x, size_y, count):
    goals = [
            Path(size_x - 1, size_y - 1, Path.Direction.x),
            Path(size_x - 1, size_y - 1, Path.Direction.y)
            ]

    routes = []
    def inner_search(base, count, history):
        if count == 0:
            if any([g == history[-1] for g in goals]):
                routes.append(history)
            return

        next_pathes = search_next_pathes(base, size_x, size_y, history)
        #print(next_pathes)
        for p in next_pathes:
            new_history = []
            new_history.extend(history)
            new_history.append(p)
            inner_search(p, count - 1, new_history)

    inner_search(base, count, [])

    return routes


SIZE_X = 5
SIZE_Y = 4

# TODO 無駄なオブジェクトを作らないようにする（再利用する）
# TODO 通った道の軌跡を線として塗り潰す必要がある
# TODO ルート情報を任意のポイントに戻せるようにしたい。途中までの探査を無駄にしないため
try:
    while True:
        count = int(input())
        routes = search_routes(Path(0, 0, None), SIZE_X, SIZE_Y, count)

        print(routes)
        print(len(routes))
except EOFError:
    pass
