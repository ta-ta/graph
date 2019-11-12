#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# グラフ描画
def graph_draw(graph: nx.MultiDiGraph):
    pos = nx.spring_layout(graph, k=0.7)

    # 重みを数値だけにする
    for _from, _to , _weight in graph.edges(data=True):
        # 重みがない時は表示しない
        if _weight.get('weight') != None:
            edge_labels = {(_from, _to): _weight['weight']}
            nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels)
        else:
            nx.draw_networkx_edges(graph, pos)

    nx.draw_networkx(graph, pos)

    # 辺が重ならないようにしたり、枠をなくしたり
    plt.tight_layout()
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    mdgraph = nx.MultiDiGraph()
    num = int(input())

    for i in range(num):
        edge_info = input().split(" ")
        from_ = int(edge_info[0])
        to_ = int(edge_info[1])
        weight_ = 0

        # 入力の確認
        if len(edge_info) != 3 and len(edge_info) != 2:
            print("Args Error")
            sys.exit()
        elif len(edge_info) == 3 :
            weight_ = int(edge_info[2])

        # 重み付きの辺を追加
        if weight_ != 0:
            mdgraph.add_weighted_edges_from([(from_, to_, weight_)])
        else:
            mdgraph.add_edges_from([(from_, to_)])

    graph_draw(mdgraph)