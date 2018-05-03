import sys
import timeit


def process_file(file):
    input_file = open(file, "r")
    dimensions = tuple(int(i) for i in input_file.readline().split())
    data = list()
    for i in range(dimensions[0]):
        data.append(tuple(int(j) for j in input_file.readline().split()))
    return dimensions, data


def is_peak(data, node):
    i, j = node
    return not ((i - 1 >= 0 and data[i - 1][j] > data[i][j]) or (i + 1 < len(data) and data[i + 1][j] > data[i][j])
                or (j - 1 >= 0 and data[i][j - 1] > data[i][j]) or (
                        j + 1 < len(data[0]) and data[i][j + 1] > data[i][j]))


def is_bottom(data, node):
    i, j = node
    return not ((i - 1 >= 0 and data[i - 1][j] < data[i][j]) or (i + 1 < len(data) and data[i + 1][j] < data[i][j])
                or (j - 1 >= 0 and data[i][j - 1] < data[i][j]) or (
                        j + 1 < len(data[0]) and data[i][j + 1] < data[i][j]))


def find_peaks(data):
    peaks = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if is_peak(data, (i, j)):
                peaks.append((i, j))
    return peaks


def find_nexts(data, current):
    nexts = []
    x, y = current
    current_value = data[x][y]
    if x - 1 >= 0 and data[x - 1][y] < current_value:
        nexts.append((x - 1, y))
    if x + 1 < len(data) and data[x + 1][y] < current_value:
        nexts.append((x + 1, y))
    if y - 1 >= 0 and data[x][y - 1] < current_value:
        nexts.append((x, y - 1))
    if y + 1 < len(data[0]) and data[x][y + 1] < current_value:
        nexts.append((x, y + 1))
    return nexts


def find_path(data, cache, node):
    x, y = node
    if cache[x][y] is None:
        if is_bottom(data, node):
            cache[x][y] = (None, 1, 0)
        else:
            nexts = find_nexts(data, node)
            for n in nexts:
                find_path(data, cache, n)
            update_node(data, cache, node, nexts)
    return cache[x][y]


def update_node(data, cache, node, nexts):
    value = data[node[0]][node[1]]
    max_drop = 0
    max_length = 0
    next_node = None
    for next in nexts:
        x, y = next
        diff = value - data[x][y] + cache[x][y][2]
        steps = cache[x][y][1] + 1
        if diff >= max_drop and steps >= max_length:
            max_drop = diff
            max_length = steps
            next_node = next
    cache[node[0]][node[1]] = (next_node, max_length, max_drop)

def main():
    dimensions, data = process_file(sys.argv[1])
    peaks = find_peaks(data)
    cache = list([[None] * dimensions[1]])
    for i in range(dimensions[0] - 1):
        cache.append(list([None] * dimensions[1]))
    start = None
    max_length = 0
    max_drop = 0
    for peak in peaks:
        x, y = peak;
        find_path(data, cache, peak)
        if cache[x][y][1] > max_length or (cache[x][y][1] == max_length and cache[x][y][2] > max_drop):
            start = peak
            max_length = cache[x][y][1]
            max_drop = cache[x][y][2]
    return start, data, cache


if __name__ == "__main__":
    start_time = timeit.default_timer()
    start, data, cache = main()
    stop_time = timeit.default_timer()
    x, y = start
    print("starting point is {} and the longest length is {} and it's corresponding drop is {}".format(start, cache[x][y][1], cache[x][y][2]))
    route = str(data[x][y])
    next = cache[x][y][0]
    while next is not None:
        x, y = next
        route += " {}".format(data[x][y])
        next = cache[x][y][0]
    print("Route: {}".format(route))
    print("Total time taken: {}".format(stop_time - start_time))
