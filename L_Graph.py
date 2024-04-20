class Vertex:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.edges = []

    def addEdge(self, edge):
        self.edges.append(edge)


class Edge:
    bracket_list = ["(", ")", "[", "]", "{", "}", "<", ">"]

    def __init__(self, to, input, output, brackets=""):
        self.to = to
        self.input = input
        self.output = output
        self.brackets = []
        temp = ""
        for c in brackets:
            if temp != "" and c in Edge.bracket_list:
                self.brackets.append(temp)
                temp = ""
            temp += c
        if temp != "":
            self.brackets.append(temp)


class L_Graph:
    open_dict = {"(": ")", "[": "]", "{": "}", "<": ">"}
    close_dict = {")": "(", "]": "[", "}": "{", ">": "<"}

    def __init__(self):
        self.vertices = []
        self.alphabet = []
        self.brackets = []
        self.stack_names = []
        self.start = None
        self.end = []

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        if vertex.type == "Start":
            if self.start == None:
                self.start = vertex
            else:
                raise Exception("Error!The graph has more than one starting vertex!")
        if vertex.type == "End":
            self.end.append(vertex)
        for e in vertex.edges:
            if e.input != "" and not e.input in self.alphabet:
                self.alphabet.append(e.input)
            for b in e.brackets:
                bracket = b[:b.index(' ')]
                if bracket not in self.brackets:
                    self.brackets.append(bracket)

    def check(self):
        if self.start == None:
            raise Exception("Error!There is no starting vertex in the graph!")
        if len(self.end) == 0:
            raise Exception("Error!There is no ending vertex in the graph!")
        for b in self.brackets:
            b_opposite = (
                L_Graph.open_dict[b[0]] + b[1:]
                if b[0] in L_Graph.open_dict
                else L_Graph.close_dict[b[0]] + b[1:]
            )
            if b_opposite not in self.brackets:
                raise Exception("Error!Brackets don't match!")

    @staticmethod
    def get_stack_name(s):
        try:
            s = s[:s.index(' ')]
        except:
            pass
        return "stack" + str(Edge.bracket_list.index(s[0]) // 2 + 1) if len(s) == 1 else "stack" + s[1:]

    def generate_stack_names(self):
        for s in self.brackets:
            stack_name = L_Graph.get_stack_name(s)
            if stack_name not in self.stack_names:
                self.stack_names.append(stack_name)
        self.stack_names.sort()

    def get_mark(self, edge):
        close_brackets = []
        for b in edge.brackets:
            if b[0] in L_Graph.close_dict:
                close_brackets.append(b)
        return (edge.input, close_brackets)

    def get_direct(self, edge, visited=None):
        res = []
        mark = self.get_mark(edge)
        if mark != ("", []):
            res.append(mark)
            return res
        if visited == None:
            visited = []
        if edge.to in visited:
            raise Exception("Error!This graph is non-deterministic!")
        else:
            visited.append(edge.to)
        for e in edge.to.edges:
            res.extend(self.get_direct(e, visited))
        if edge.to.type == "End":
            res.append(("", []))
        return res
    
    def check_deterministic_one_step(self, vertex):
        marks = []
        for edge in vertex.edges:
            # close_brackets = []
            # for b in e.brackets:
            #     if b[0] in L_Graph.close_dict:
            #         close_brackets.append(b)
            # path = (e.input, close_brackets)
            mark = self.get_mark(edge)
            if mark in marks:
                return False
            else:
                marks.append(mark)
        return True

    def check_deterministic_two_step(self, vertex):
        direct_all = []
        for edge in vertex.edges:
            direct = self.get_direct(edge, [vertex])
            for d in direct:
                if d not in direct_all:
                    direct_all.append(d)
                else:
                    if d != ("", []):
                        raise Exception("Error!This graph is non-deterministic!")
                    # raise Exception("Error!This graph is non-deterministic!")
    
    def check_deterministic(self, vertex):
        if not self.check_deterministic_one_step(vertex):
            self.check_deterministic_two_step(vertex)
            # raise Exception("Error!This graph is non-deterministic!")