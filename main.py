import argparse
import logging
import sys

import networkx as nx


LOGGER = 'graph'
logger = logging.getLogger(LOGGER)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s %(lineno)s: %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


INF = 2**30
EDGES = 'edges'
MATRIX = 'matrix'


class FileLine():
    # ファイルの中身を配列として格納
    def __init__(self, lines):
        self.lines = lines
        self.number_of_line = len(lines)
        self.line_counter = 0

    def next_input_line(self):
        # 次の1行を返す
        if self.line_counter >= self.number_of_line:
            logger.warning('no next line')
            return ""
        next_line = self.lines[self.line_counter]
        self.line_counter += 1
        return next_line

def convert_to_edges(adjacency_matrix):
    # 隣接行列を枝リストに変換
    edges = []
    for from_, row in enumerate(adjacency_matrix):
        for to_, is_connect in enumerate(row):
            if is_connect > 0:
                # is_connect は0,1以外(=重み)の場合もありうる
                edges.append([from_, to_, is_connect])
    return edges

def remove_weight(edges):
    # convert_to_edges() による変換では重みが付与されているため、重みなしの場合は取り除く
    non_weight_edges = []
    for from_, to_, _ in edges:
        non_weight_edges.append([from_, to_])
    return non_weight_edges

def input_and_format(get, expression=EDGES, weighted=False, drawed_min_index=0):
    # 点数, 枝数の入力
    # expression により形式は異なる
    meta = [int(d) for d in get().split()]
    if expression == EDGES:
        number_of_vertice, number_of_edges = meta
        edges = []
        min_index = INF
        for i in range(number_of_edges):
            try:
                edge = [int(d) for d in get().split()]
            except ValueError as err:
                logger.error(err)
                sys.exit()
            if len(edge) == 2 or len(edge) == 3:
                min_index = min(min_index, edge[0], edge[1])
                edges.append(edge)
            else:
                logger.error('invalid data format')
                sys.exit()
    elif expression == MATRIX:
        number_of_vertice = meta[0]
        adjacency_matrix = []
        min_index = 0
        for i in range(number_of_vertice):
            try:
                connect_row = [int(d) for d in get().split()]
            except ValueError as err:
                logger.error(err)
                sys.exit()
            if len(connect_row) == number_of_vertice:
                adjacency_matrix.append(connect_row)
            else:
                logger.error('invalid data format')
                sys.exit()
        edges = convert_to_edges(adjacency_matrix)
        if weighted == False:
            edges = remove_weight(edges)

    # index の調整
    for idx, edge in enumerate(edges):
        edges[idx][0] = edge[0] - (min_index - drawed_min_index)
        edges[idx][1] = edge[1] - (min_index - drawed_min_index)
    return edges

def display_edges(edges):
    # debug用に表示
    for e in edges:
        print(e)


if __name__ == '__main__':
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', help='setting input file', type=str, default='')
    parser.add_argument('-w', '--weighted', help='drawing weighted graph', action='store_true')
    parser.add_argument('-d', '--directed', help='drawing directed graph', action='store_true')
    parser.add_argument('-e', '--expression', help='setting input graph expression [edges, matrix] (default: edges)', default=EDGES, type=str)
    parser.add_argument('-i', '--index', help='setting minimum index', type=int, default=0)

    args = parser.parse_args()
    input_file = args.file
    weighted = args.weighted
    directed = args.directed
    expression = args.expression
    drawed_min_index = args.index
    if expression not in [EDGES, MATRIX]:
        logger.warning('--expression option has to be selected from [edges, matrix]')
        sys.exit()

    # input
    if input_file == '':
        # std input
        edges = input_and_format(input, expression=expression, drawed_min_index=drawed_min_index)
    else:
        # file input
        try:
            with open(input_file) as f:
                lines = f.readlines()
        except FileNotFoundError as err:
            logger.error(err)
            sys.exit()
        else:
            file_line = FileLine(lines)
            edges = input_and_format(file_line.next_input_line, expression=expression, weighted=weighted, drawed_min_index=drawed_min_index)

    # 有向無向
    if directed == True:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()
    
    # nx用にフォーマット修正
    nx_edges = []
    if weighted == True:
        for edge in edges:
            if len(edge) == 3:
                from_, to_, weight_ = edge
                nx_edges.append((from_, to_, {"label": weight_}))
            else:
                logger.error('invalid data format')
                sys.exit()
    else:
        for edge in edges:
            if len(edge) == 2:
                nx_edges.append(tuple(edge))
            else:
                logger.error('invalid data format')
                sys.exit()
    graph.add_edges_from(nx_edges)
    nx.nx_agraph.view_pygraphviz(graph)

    # 枝の確認
    # display_edges(nx_edges)