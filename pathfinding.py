from collections import deque # a line (queue) you can add to and take from quickly

def is_near_fire(cell): # True if any neighbor is on fire
    for neighbor in cell.get_neighbors():
        if neighbor.is_fire:
            return True
    return False

def find_path(start_cell, avoid_near_fire=False): # Breadth-First Search from start_cell to the button, avoiding blocked cells and cells on fire right now
    # if avoid_near_fire is True, also avoid cells next to fire
    queue = deque([start_cell]) # cells we still need to look at, closest first
    came_from = {start_cell: None} # remembers which cell we came from to reach each cell

    while queue:
        current = queue.popleft() # take the next cell in line
        if current.is_button: # found it, walk backwards to build the path
            path = []
            while current != start_cell:
                path.append(current)
                current = came_from[current] # step back one cell
            path.reverse() # flip it so it goes start -> button
            return path

        for neighbor in current.get_neighbors(): # look at each cell next to this one
            if neighbor not in came_from and neighbor.is_open and not neighbor.is_fire: # not visited, open, not burning
                if avoid_near_fire and is_near_fire(neighbor):
                    continue # too close to fire, skip it
                came_from[neighbor] = current # remember how we got here
                queue.append(neighbor) # look at it later

    return None # no safe path exists
