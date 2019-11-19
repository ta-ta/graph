#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from PIL import Image

WEIGHTED = False

# グラフ描画
def graph_draw(graph: nx.MultiDiGraph):
    pos = nx.spring_layout(graph)

    nx.draw_networkx(graph, pos)

    ag = nx.nx_agraph.to_agraph(graph)
    ag.layout()
    ag.draw("graph.png")

    # 画像の読み込み
    image = Image.open("graph.png")
    image_list = np.asarray(image)

    plt.imshow(image_list)
    plt.tight_layout()
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', help='problem file', type=str)
    parser.add_argument('-w', '--weighted', help='Existence of weight(def:None)', action='store_true')
    parser.add_argument('-f', '--format', help='Input format is edges or matrix(def:edges)', default='edges', type=str)
    parser.add_argument('-d', '--directed', help='Directed or UnDirected(def:Undirected)', action='store_true')
    parser.add_argument('-t', '--index_transform', help='1-indexed transform 0-indexed(def:No)', action='store_true')

    args = parser.parse_args()
    problem_file = args.file

    WEIGHTED = args.weighted
    format_ = args.format
    directed_ = args.directed
    indexed_ = args.index_transform

    # 有向
    if directed_ == True:
        m_graph = nx.MultiDiGraph()
    # 無向
    else:
        m_graph = nx.MultiGraph()

    # ファイル指定
    if problem_file != None:
        # 頂点の数を取得
        with open(problem_file) as f:
            nodes = int(f.readline().split(' ')[0])
            
            for i in range(nodes - 1):
                edge_info = f.readline().split(' ')
                edges = [int(e_i) for e_i in edge_info]

                # 始点、終点
                from_ = edges[0]
                to_ = edges[1]

                # 重みあり
                if WEIGHTED == True:
                    weight_ = edges[2]
                    # 辺を追加
                    m_graph.add_edges_from([(from_, to_, {"label": weight_})])
                else:
                    m_graph.add_edges_from([(from_, to_)])
    # ファイル指定なしの場合は標準入力に従う
    else:
        # マトリックス
        if format_ == 'matrix':
            print('matrix')
            exit()
        # 枝リスト
        else:
            for i in range(int(input())):
                edge_info = input().split(' ')
                edges = [int(e_i) for e_i in edge_info]
                
                # 始点、終点
                from_ = edges[0]
                to_ = edges[1]

                # 重みあり
                if WEIGHTED == True:
                    weight_ = edges[2]
                    m_graph.add_edges_from([(from_, to_, {'label': weight_})])
                else:
                    m_graph.add_edges_from([(from_, to_)])

    # グラフ描画
    graph_draw(m_graph)