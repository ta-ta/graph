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
    ag.node_attr['shape'] = 'circle'
    ag.layout()
    ag.draw("graph.png")

    # 画像の読み込み
    image = Image.open("graph.png")
    image_list = np.asarray(image)

    plt.imshow(image_list)
    plt.tight_layout()
    plt.axis("off")
    plt.show()

# 行列の解析
def matrix_analyze(count: int, mat: list, graph: nx.MultiDiGraph):
    for i in range(count):
        for j in range(count):
            # 始点、終点
            from_ = 0
            to_ = 0

            # 隣接していない場合は処理なし
            if mat[i][j] != 0:
                from_ = i + 1
                to_ = j + 1
            else:
                continue

            # 変換有無
            if indexed_ == True:
                # 変換あり
                from_ = i
                to_ = j
                
            # 重み有無
            if WEIGHTED == True:
                # 重みあり
                weight_ = mat[i][j]
                graph.add_edges_from([(from_, to_, {'label': weight_})])
            else:
                # 重みなし
                graph.add_edges_from([(from_, to_)])

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

    # 有向/無向の判定
    if directed_ == True:
        # 有向
        m_graph = nx.MultiDiGraph()
    else:
        # 無向
        m_graph = nx.MultiGraph()

    # ファイル指定の有無
    if problem_file != None:
        # ファイル指定あり
        with open(problem_file) as f:
            file_info = f.readlines()
        count = file_info[0]

        # 形式の判定
        if len(count.split(' ')) == 1:
            # マトリックス
            node_count = int(count.split(' ')[0])

            # 隣接行列の設定
            matrix = [[0 for i in range(node_count)] for j in range(node_count)]
            for i in range(node_count):
                edge_info = file_info[i + 1].split(' ')

                # 要素が不足していないかどうか
                if len(edge_info) != node_count:
                    print('input error')
                    exit()
                
                for j in range(node_count):
                    matrix[i][j] = int(edge_info[j])

            # 行列の解析
            matrix_analyze(node_count, matrix, m_graph)
        else:
            # 枝リスト
            node_count = int(count.split(' ')[0])

            # 枝リスト取得
            for i in range(1, node_count):
                edges = file_info[i].split(' ')

                # 変換有無
                if indexed_ == True:
                    # 変換あり
                    from_ = int(edges[0]) - 1
                    to_ = int(edges[1]) - 1
                else:
                    # 変換なし
                    from_ = int(edges[0])
                    to_ = int(edges[1])
                m_graph.add_edges_from([(from_, to_)])
    else:
        # 標準入力の指定
        if format_ == 'matrix':
            # マトリックス
            node_count = int(input())

            # 隣接行列の設定
            matrix = [[0 for i in range(node_count)] for j in range(node_count)]
            for i in range(node_count):
                edge_info = input().split(' ')

                # 要素が不足していないかどうか
                if len(edge_info) != node_count:
                    print('input error')
                    exit()
                
                for j in range(node_count):
                    matrix[i][j] = int(edge_info[j])

            # 行列の解析
            matrix_analyze(node_count, matrix, m_graph)
        else:
            # 枝リスト
            node_edge = input()
            node_count = int(node_edge.split(' ')[0])
            edge_count = int(node_edge.split(' ')[1])

            for i in range(edge_count):
                edge_info = input().split(' ')
                edges = [int(e_i) for e_i in edge_info]
                
                # 変換有無
                if indexed_ == True:
                    # 変換あり
                    from_ = edges[0] - 1
                    to_ = edges[1] - 1
                else:
                    # 変換なし
                    from_ = edges[0]
                    to_ = edges[1]

                # 頂点チェック
                if (node_count < from_) or (node_count < to_):
                    print('node error')
                    exit()

                # 重み有無
                if WEIGHTED == True:
                    # 重みあり
                    weight_ = edges[2]
                    m_graph.add_edges_from([(from_, to_, {'label': weight_})])
                else:
                    # 重みなし
                    m_graph.add_edges_from([(from_, to_)])

    # グラフ描画
    graph_draw(m_graph)