import math
import pymysql
import tkinter as tk
import tkinter.messagebox
import pandas as pd
import queue
import copy

max_priority = 10
sort_list = []


class Reversor:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return other.value < self.value

class Node:
    def __init__(self, name, quantity, start_date, end_date, priority):
        self.name = name
        self.quantity = quantity
        self.start_date = start_date
        self.end_date = end_date
        self.children = []
        self.priority = priority

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_name(self):
        return self.name

    def get_child(self):
        return self.children


def submit():
    product_name.append(entry_name.get())
    product_date.append(entry_date.get())
    product_quantity.append(entry_quantity.get())
    if not entry_name.get() or not entry_date.get() or not entry_quantity.get():
        tk.messagebox.showinfo("info", "请输入信息")
    else:
        entry_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        text1 = "%s  %s  %s\n" % (product_name[len(product_date) - 1], product_quantity[len(product_date) - 1],
                                  product_date[len(product_date) - 1])
        text.insert(tk.END, text1)


def build_tree(tree_relation):
    q = queue.Queue()
    node_list = []
    root = Node(tree_relation[0][0], 0, None, None, max_priority)
    node_list.append(root)
    q.put(root)
    pos = 0
    while not q.empty():
        top = q.get()
        while pos != len(tree_relation):
            if tree_relation[pos][0] != top.get_name():
                break

            # 每个物料在排序时的优先级
            top.priority = max_priority - int(tree_relation[pos][2] if tree_relation[pos][2] is not None else 0)

            child = Node(tree_relation[pos][1], 0, None, None, 0)
            top.add_child(child)
            node_list.append(child)
            q.put(child)
            pos += 1

    return node_list


# father 是父节点， node是当前节点， father为None时是根节点

def dfs(father, node):
    if node is None:
        return

    if father is None:

        start_time = product_date[product_name.index(node.name)]
        quantity = product_quantity[product_name.index(node.name)]

        time_delta = find(mat_time, lambda x: x[0] == node.name)

        node.quantity = int(quantity)

        node.end_date = pd.to_datetime(start_time).strftime('%Y-%m-%d')
        node.start_date = (pd.to_datetime(node.end_date) - pd.to_timedelta(int(time_delta[3]), unit='D')).strftime('%Y-%m-%d')
        sort_list.append(node)
        for i in node.get_child():
            dfs(node, i)

    else:

        time_delta = find(mat_time, lambda x: x[0] == node.name)

        num = find(ass, lambda x: x[0] == father.name and x[1] == node.name)[2]
        need = father.quantity * num
        losses = find(loss, lambda x: x[0] == node.name)[1]
        l = 1 - losses
        need = math.ceil(need / l)
        node.quantity = need


        node.end_date = father.start_date
        node.start_date = (pd.to_datetime(node.end_date) - pd.to_timedelta(int(sum(time_delta[1:])), unit='D')).strftime('%Y-%m-%d')
        sort_list.append(node)

        for i in node.get_child():
            dfs(node, i)


def find(node, func):
    for i in node:
        if func(i):
            return i


def get_answer():
    node_list = build_tree(tree_relation)

    # yanjing = copy.deepcopy(find(node_list, lambda x: x.get_name() == '眼镜'))
    # jingkuang = copy.deepcopy(find(node_list, lambda x: x.get_name() == '镜框'))

    product_trees = [copy.deepcopy(find(node_list, lambda x: x.get_name() == i)) for i in product_name]
    for tree in product_trees:
        dfs(None, tree)

    sorted_list = sorted(sort_list, key=lambda x: (x.priority, Reversor(x.start_date)), reverse=True)

    for i in sorted_list:
        # 如果有库存，则改变所有子节点的需要量，最后自己减去库存
        father_storage = find(fac, lambda x: x[0] == i.name)
        s = father_storage
        q = i.quantity
        i.quantity = max(i.quantity - father_storage[1], 0)
        father_storage[1] = max(0, father_storage[1] - q)
        # print(i.name, s)

        if s != 0:

            for child in i.children:
                num = find(ass, lambda x: x[0] == i.name and x[1] == child.name)[2]
                need = i.quantity * num
                losses = find(loss, lambda x: x[0] == child.name)[1]
                l = 1 - losses
                need = math.ceil(need / l)
                child.quantity = need





    output_list = sorted(sorted_list, key=lambda x: x.start_date)
    method_ = {"buy": "采购", "produce": "生产"}
    text1 = "%s\t%s\t%s\t%s\t%s\n" % ("名称", "调配方式", "数量", "开始日期", "结束日期")
    text_result.insert(tk.END, text1)
    for i in output_list:
        print(i.name, i.start_date, i.end_date, i.quantity)
        method = find(way, lambda x: x[0] == i.name)[1]
        text1 = "%s\t%s\t%s\t%s\t%s\n" % (i.name, method_[method], i.quantity, i.start_date, i.end_date)
        text_result.insert(tk.END, text1)



db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Fjh57593980', db='erp')
cursor = db.cursor()

cursor.execute(
    "select 父物料名称, 子物料名称, 层次 from 调配构成表 left outer join bom on 调配构成表.父物料名称 = bom.描述")
tree_relation = cursor.fetchall()

cursor.execute(
    "select distinct 名称, 配料提前期, 供应商提前期, 作业提前期 from 物料表 left outer join 调配构成表 on 调配构成表.子物料名称 = 物料表.名称")
mat_time = cursor.fetchall()

cursor.execute("select 父物料名称, 子物料名称, 构成数 from 调配构成表")
ass = cursor.fetchall()

cursor.execute("select 物料名称, (库存表.工序库存 + 库存表.资材库存) from 库存表, 物料表 where 库存表.物料号 = 物料表.物料名 ")
fac = cursor.fetchall()
fac = [list(i) for i in fac]

cursor.execute("select 名称, 损耗率 from 物料表")
loss = cursor.fetchall()

cursor.execute("select 名称, 调配方式 from 物料表")
way = cursor.fetchall()

win = tk.Tk()
win.title("ERP系统")
win.geometry("500x500")
label = tk.Label(win, text="ERP系统", font=('Times', 24)).place(x=180, y=20)
entry_name = tk.Entry(win)
entry_name.place(x=70, y=80)
label_name = tk.Label(win, text="产品名称")
label_name.place(x=10, y=80)
label_quantity = tk.Label(win, text="需求数量")
label_quantity.place(x=10, y=130)
entry_quantity = tk.Entry(win)
entry_quantity.place(x=70, y=130)
label_date = tk.Label(win, text="完工时间")
label_date.place(x=10, y=180)
entry_date = tk.Entry(win)
entry_date.place(x=70, y=180)

# 测试
entry_name.insert(0, '眼镜')
entry_quantity.insert(0, '100')
entry_date.insert(0, '2020-5-30')

product_name = []
product_quantity = []
product_date = []

label_plan = tk.Label(win, text="订单列表").place(x=345, y=60)
text = tk.Text(win)
text.configure(height=12, width=30)
text.place(x=265, y=90)

button = tk.Button(win, text="添加订单", command=submit).place(x=70, y=230)

text_result = tk.Text(win)
text_result.configure(height=12, width=65)
text_result.place(x=20, y=295)

button_result = tk.Button(win, text="计算结果", command=get_answer).place(x=210, y=260)

win.mainloop()
