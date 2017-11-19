# Алгоритм: строим по регулярному выражению автомат, после чего перебираем слово начиная с начала, каждый раз уменьшая суффикс и проверяем подслово на принадлежность языку

#Khromov Igor


class StackException(Exception):
    pass


class Node:
    def __init__(self):
        self.transitions = []
        for _ in range(4):
            self.transitions.append([])


index = {
    '1': 0,
    'a': 1,
    'b': 2,
    'c': 3
}


class Automation:

    def __init__(self, start=None, finish=None, s=None):

        self.start = Node() if start is None else start
        self.finish = Node() if finish is None else finish
        if not s is None:
            self.start.transitions[index[s]].append(self.finish)

    def klenee(self):
        new_start = Node()
        new_start.transitions[0].append(self.start)
        self.finish.transitions[0].append(new_start)
        self.start = new_start
        self.finish = new_start


def concat_automata(a1, a2):
    a1.finish.transitions[0].append(a2.start)
    to_return = Automation(a1.start, a2.finish)
    return to_return

def union_automata(a1, a2):
    new_start = Node()
    new_finish = Node()
    new_start.transitions[0].append(a1.start)
    new_start.transitions[0].append(a2.start)
    a1.finish.transitions[0].append(new_finish)
    a2.finish.transitions[0].append(new_finish)
    to_return = Automation(new_start, new_finish)
    return to_return


def get_epsilon_nodes(node, ans):
    trans = node.transitions[0]
    for tran in trans:
        if not tran in ans:
            ans.append(tran)
            ans = get_epsilon_nodes(tran, ans)
    return ans


def get_possible_nodes(node, ind, ans):
    eps_nodes = []
    eps_nodes = get_epsilon_nodes(node, eps_nodes)
    for eps_node in eps_nodes:
        trans = eps_node.transitions[ind]
        for tran in trans:
            if not tran in ans:
                ans.append(tran)
    for transition in node.transitions[ind]:
        ans.append(transition)
    return ans


def check_string(a, s):
    nodes = [a.start]
    for symb in s:
        new_lvl_nodes = []
        for node in nodes:
            buff = []
            buff = get_possible_nodes(node, index[symb], buff)
            new_lvl_nodes.extend(buff)
        new_lvl_nodes = list(set(new_lvl_nodes))
        if len(new_lvl_nodes) == 0:
            return False
        nodes = new_lvl_nodes

    t = len(nodes)
    for i in range(t):
        nodes = get_epsilon_nodes(nodes[i], nodes)

    for node in nodes:
        if node == a.finish:
            return True

    return False


def get_max_suffix_length(a, s):
    for i in range(len(s)):
        res = check_string(a, s[i:len(s)])
        if res:
            return s[i:len(s)], len(s) - i


def main():
    alpha = input()
    stack = []
    try:
        for symb in alpha:
            if symb == '.':
                if len(stack) < 2:
                    raise StackException("Wrong arguments on concatenation")
                second = stack.pop()
                first = stack.pop()
                res = concat_automata(first, second)
                stack.append(res)
            elif symb == '+':
                if len(stack) < 2:
                    raise StackException("Wrong arguments on union")
                second = stack.pop()
                first = stack.pop()
                res = union_automata(first, second)
                stack.append(res)
            elif symb == '*':
                if len(stack) < 1:
                    raise StackException("Wrong arguments on kleene operator")
                stack[-1].klenee()
            else:
                a = Automation(s=symb)
                stack.append(a)
    except StackException:
        print("Wrong exception")
        return
    if len(stack) != 1:
        print("Incorrect expression " + str(len(stack)))
        return

    result = stack[-1]
    s = input()
    suff, suff_len = get_max_suffix_length(result, s)
    print("Maximum suffix is '{}', with length {}".format(suff, suff_len))
    return


if __name__ == "__main__":
    main()
