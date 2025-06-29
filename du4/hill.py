from collections import deque
import sys

class State:
    def __init__(self, prev, slope, steps):
        self.prev  = prev
        self.slope = slope
        self.steps = steps
def neighbors(pos, max_rows, max_cols):
    x, y = pos
    for dx, dy in [(-1,0),(0,-1),(0,1),(1,0)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < max_rows and 0 <= ny < max_cols:
            yield nx, ny
def path_traceback(rec, start):
    seq = []
    cur = start
    while cur is not None:
        seq.append(cur)
        cur = rec[cur[0]][cur[1]].prev
    return seq
def bfs_elevation(grid, remap, comp):
    R, C = len(grid), len(grid[0])
    tracker = [[State((0,0), -1, -1) for _ in range(C)] for _ in range(R)]
    sx, sy = remap(0,0)
    tracker[sx][sy].slope = 0
    tracker[sx][sy].steps = 0
    tracker[sx][sy].prev  = None
    from collections import deque
    q = deque([(sx,sy)])
    while q:
        x,y = q.popleft()
        for nx,ny in neighbors((x,y), R, C):
            if grid[nx][ny] > grid[x][y]:
                new_slope = max(tracker[x][y].slope, grid[nx][ny]-grid[x][y])
                new_steps = tracker[x][y].steps + 1
                st = tracker[nx][ny]
                if (st.slope==-1
                    or comp(new_steps, st.steps)
                    or (new_steps==st.steps and comp(st.slope, new_slope))):
                    st.slope = new_slope
                    st.steps = new_steps
                    st.prev  = (x,y)
                    q.append((nx,ny))
    return tracker
def find_optimal_path(grid, comp):
    R, C = len(grid), len(grid[0])
    asc  = bfs_elevation(grid, lambda x,y:(x,y),           comp)
    des  = bfs_elevation(grid, lambda x,y:(R-1-x,C-1-y),  comp)
    best_h = None
    best_s = None
    tgt    = None
    for i in range(R):
        for j in range(C):
            a = asc[i][j]
            d = des[i][j]
            if a.slope!=-1 and d.slope!=-1:
                h = max(a.slope, d.slope)
                if (best_s is None
                    or grid[i][j] > best_h
                    or (grid[i][j]==best_h and comp(best_s, h))):
                    best_h = grid[i][j]
                    best_s = h
                    tgt    = (i,j)
    if tgt is None:
        return None
    up   = path_traceback(asc,  tgt)[1:][::-1]
    down = path_traceback(des, tgt)
    return up + down
def display_path(grid, path):
    if path is None or len(path)==0:
        print("Error: Cesta neexistuje!", file=sys.stderr)
        sys.exit(1)
    print(len(path))
    print(" ".join(str(grid[x][y]) for x,y in path))
def main():
    argc = len(sys.argv)
    mode = None
    if argc == 2:
        if sys.argv[1] in ("lift","piste"):
            mode = sys.argv[1]
    try:
        dims = sys.stdin.readline().split()
        R, C = int(dims[0]), int(dims[1])
    except:
        print("Error: Chybny vstup!", file=sys.stderr)
        sys.exit(1)
    terrain = []
    for _ in range(R):
        line = sys.stdin.readline()
        if not line:
            print("Error: Chybny vstup!", file=sys.stderr)
            sys.exit(1)
        parts = line.split()
        if len(parts)!=C:
            print("Error: Chybny vstup!", file=sys.stderr)
            sys.exit(1)
        try:
            terrain.append(list(map(int, parts)))
        except:
            print("Error: Chybny vstup!", file=sys.stderr)
            sys.exit(1)
    if mode is None:
        display_path(terrain, find_optimal_path(terrain, lambda a,b: a<b))
        display_path(terrain, find_optimal_path(terrain, lambda a,b: a>b))
    elif mode=="lift":
        display_path(terrain, find_optimal_path(terrain, lambda a,b: a<b))
    else:
        display_path(terrain, find_optimal_path(terrain, lambda a,b: a>b))
    sys.exit(0)
if __name__=="__main__":
    main()