import sys
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# グラフ描画
def graph_draw(g: nx.MultiDiGraph):
    pos = nx.spring_layout(g, k=0.7)

    # 重みを数値だけにする
    for i, j ,w in g.edges(data=True):
        # 表示をなくすために書き換え
        if w['weight'] == 0:
            w['weight'] = ""

        edge_labels = {(i, j): w['weight']}
        nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)

    nx.draw_networkx(g, pos)

    # 辺が重ならないようにしたり、枠をなくしたり
    plt.tight_layout()
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    flg = True  # エラーチェック
    G = nx.MultiDiGraph()

    for i in range(int(input())):
        weighted = False
        data = input()
        data_group = data.split(" ")
        from_ = to_ = weight_ = 0

        # 入力の確認
        if len(data_group) == 2:
            from_ = int(data_group[0])
            to_ = int(data_group[1])
        elif len(data_group) == 3:
            from_ = int(data_group[0])
            to_ = int(data_group[1])
            weight_ = int(data_group[2])
        else:
            print("Args Error")
            flg = False
            break

        # 重み付きの辺を追加
        G.add_weighted_edges_from([(from_, to_, weight_)])

    if flg == True:
       graph_draw(G)