from string import Template
from L_Graph import *


class CodeGenerator:
    def __init__(self, l_graph):
        self.beginning = Template(open("./template/beginning.tmpl", "r").read())
        self.def_stack = Template(open("./template/def_stack.tmpl", "r").read())
        self.loop_start = Template(open("./template/loop_start.tmpl", "r").read())
        self.main = Template(open("./template/main.tmpl", "r").read())
        self.vertex = Template(open("./template/vertex.tmpl", "r").read())
        self.edge_condition = Template(
            open("./template/edge_condition.tmpl", "r").read()
        )
        self.undo_read = Template(open("./template/undo_read.tmpl", "r").read())
        self.push = Template(open("./template/push.tmpl", "r").read())
        self.pop = Template(open("./template/pop.tmpl", "r").read())
        self.output = Template(open("./template/output.tmpl", "r").read())
        self.toAnotherVertex = Template(
            open("./template/toAnotherVertex.tmpl", "r").read()
        )
        self._continue = Template(open("./template/continue.tmpl", "r").read())
        self.exception = Template(open("./template/exception.tmpl", "r").read())
        self.end = Template(open("./template/end.tmpl", "r").read())
        self.code = []
        self.l_graph = l_graph

    def get_condition(
        self,
        input,
        brackets,
    ):
        if input == "":
            conditions = []
        else:
            conditions = ["c == '" + input + "'"]
        stack_dict = {}
        for bracket in brackets:
            if bracket[0] in L_Graph.close_dict:
                stack_name = L_Graph.get_stack_name(bracket)
                if stack_name not in stack_dict:
                    stack_dict[stack_name] = 1
                else:
                    stack_dict[stack_name] += 1
                condition = "len(" + stack_name + ") > "
                pre = condition + str(stack_dict[stack_name] - 2)
                cur = condition + str(stack_dict[stack_name] - 1)
                try:
                    idx = conditions.index(pre)
                except ValueError:
                    conditions.append(cur)
                else:
                    conditions[idx] = cur
                pos = bracket.index(' ')
                if pos < len(bracket) - 1:
                    condition = (
                        stack_name
                        + "[-"
                        + str(stack_dict[stack_name])
                        + "] == '"
                        + bracket[pos + 1:]
                        + "'"
                    )
                    conditions.append(condition)
        return " and ".join(conditions)

    def generate_commands(
        self,
        vertex,
        edge,
        input,
        brackets,
        res_file,
        indentation="    ",
        empty_edge=False,
        unique=True,
    ):
        if empty_edge or input == "":
            self.code.append(self.undo_read.substitute(indentation=indentation))
        for bracket in brackets:
            if bracket[0] in L_Graph.open_dict:
                pos = bracket.index(' ')
                self.code.append(
                    self.push.substitute(
                        indentation=indentation,
                        stack_name=L_Graph.get_stack_name(bracket),
                        symbol=bracket[pos + 1:] if pos < len(bracket) - 1 else '',
                    )
                )
            elif bracket[0] in L_Graph.close_dict:
                if empty_edge:
                    continue
                self.code.append(
                    self.pop.substitute(stack_name=L_Graph.get_stack_name(bracket))
                )
        if edge.output != "":
            self.code.append(
                self.output.substitute(indentation=indentation, symbol=edge.output)
            )
        if edge.to != vertex:
            self.code.append(
                self.toAnotherVertex.substitute(
                    indentation=indentation, new_vertex=edge.to.name
                )
            )
        if not (empty_edge and unique):
            self.code.append(self._continue.substitute())
        res_file.writelines(self.code)
        self.code.clear()

    def generate_if_block(self, vertex, edge, res_file, empty_edge=False, unique=True):
        if empty_edge:
            if unique:
                self.generate_commands(
                    vertex, edge, edge.input, edge.brackets, res_file, "", True
                )
            else:
                direct = self.l_graph.get_direct(edge)
                direct.sort(key=lambda x: len(x[1]), reverse=True)
                for d in direct:
                    if d == ("", []):
                        continue
                    condition = self.get_condition(d[0], d[1])
                    self.code.append(
                        self.edge_condition.substitute(condition=condition)
                    )
                    self.generate_commands(
                        vertex,
                        edge,
                        d[0],
                        d[1],
                        res_file,
                        empty_edge=True,
                        unique=False,
                    )
        else:
            if unique:
                condition = self.get_condition(edge.input, edge.brackets)
                self.code.append(self.edge_condition.substitute(condition=condition))
                self.generate_commands(
                    vertex, edge, edge.input, edge.brackets, res_file
                )
            else:
                raise Exception("Error!This graph is non-deterministic!")

    def generate(self):
        # Generate the names of stacks.
        self.l_graph.check()
        self.l_graph.generate_stack_names()

        res_file = open("result.py", "w")

        # Generate the beginning of the code.
        startVertexName = self.l_graph.start.name
        self.code.append(
            self.beginning.substitute(
                alphabet=str(self.l_graph.alphabet), start=startVertexName
            )
        )
        res_file.writelines(self.code)
        self.code.clear()

        # Define stacks.
        for stack_name in self.l_graph.stack_names:
            self.code.append(self.def_stack.substitute(stack_name=stack_name))
        res_file.writelines(self.code)
        self.code.clear()

        # Loop starts.
        self.code.append(self.loop_start.substitute())
        res_file.writelines(self.code)
        self.code.clear()

        for v in self.l_graph.vertices:
            self.l_graph.check_deterministic(v)
            self.code.append(self.vertex.substitute(vertex_name=v.name))
            res_file.writelines(self.code)
            self.code.clear()

            # Store the edges that are not empty edges into edges_list. Edges with inputs have higher priority and they should be at the front.
            empty_edges = []
            edges_list = []
            empty_stack_edges = []
            empty_input_edges = []
            mark_dict = {}
            for e in v.edges:
                empty_edge = True
                if e.input != "":
                    empty_edge = False
                else:
                    for bracket in e.brackets:
                        if bracket[0] in L_Graph.close_dict:
                            empty_edge = False
                            break
                if empty_edge:
                    empty_edges.append(e)
                    continue
                else:
                    # empty_input_edges.append(e)
                    mark = self.l_graph.get_mark(e)
                    if mark[0] != "" and mark[1] != []:
                        edges_list.append(e)
                    elif mark[1] == []:
                        empty_stack_edges.append(e)
                    else:
                        empty_input_edges.append(e)
                    key = (mark[0], ''.join(mark[1]))
                    if key not in mark_dict:
                        mark_dict[key] = 1
                    else:
                        mark_dict[key] += 1
            edges_list.extend(empty_stack_edges)
            edges_list.extend(empty_input_edges)

            # Traverse edges_list and generate the code of the if block corresponding to each edge.
            for edge in edges_list:
                unique = True
                mark = self.l_graph.get_mark(edge)
                key = (mark[0], ''.join(mark[1]))
                # if edge.input != "" and mark_dict[key] > 1:
                #     unique = False
                if mark_dict[key] > 1:
                    unique = False
                self.generate_if_block(v, edge, res_file, False, unique)

            # Handle empty edges and add exceptions.
            if v.type == "End":
                if len(empty_edges) > 0:
                    for ee in empty_edges:
                        self.generate_if_block(v, ee, res_file, True, False)
                    # raise Exception("This may lead to non-determinism.")
                stack_checking = ''
                for stack_name in self.l_graph.stack_names:
                    stack_checking += ' or '
                    stack_checking += 'len(' + stack_name + ') != 0'
                self.code.append(self.end.substitute(condition=stack_checking))
                res_file.writelines(self.code)
                self.code.clear()
            else:
                if len(empty_edges) > 0:
                    if len(empty_edges) == 1:
                        self.generate_if_block(v, empty_edges[0], res_file, True)
                    else:
                        for ee in empty_edges:
                            self.generate_if_block(v, ee, res_file, True, False)
                        self.code.append(self.exception.substitute())
                        res_file.writelines(self.code)
                        self.code.clear()
                else:
                    self.code.append(self.exception.substitute())
                    res_file.writelines(self.code)
                    self.code.clear()

        self.code.append(self.main.substitute())
        res_file.writelines(self.code)

        res_file.close()
        print("Code successfully generated!")
