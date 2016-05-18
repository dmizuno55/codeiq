from enum import Enum

class Path:
    Direction = Enum('Direction', 'x y')
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        
    def can_go_to(self, x, y, direction):
        if self.direction == direction:
            return False
        if self.direction == Path.Direction.x:
            if self.x != x:
                return False
        if self.direction == Path.Direction.y:
            if self.y != y:
                return False
        return True
        
    def go_to_x(self, x):
        if not self.can_go_to(x, self.y, Path.Direction.x):
            raise Exception('invalid path')
        return Path(x, self.y, Path.Direction.x)
        
    def go_to_y(self, y):
        if not self.can_go_to(self.x, y, Path.Direction.y):
            raise Exception('invalid path')
        return Path(self.x, y, Path.Direction.y)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{{x: {0}, y: {1}, d: {2}}}'.format(self.x, self.y, self.direction.name)


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

def search_routes(base, size_x, size_y, count):
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
