from flask import Flask, request, send_from_directory
from flask_cors import CORS
from CodeGenerator import *
from L_Graph import *

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/download", methods=["GET", "POST"])
def getData():
    # if request.method == 'POST':
    #     post_data = request.get_json()
    #     print(post_data)
    #     try:
    #         generateCode(post_data)
    #     except Exception as e:
    #         return str(e)
    # return send_from_directory('./', 'result.py', as_attachment=True)
    if request.method == "POST":
        post_data = request.get_json()
        print(post_data)
        try:
            generateCode(post_data)
        except Exception as e:
            return str(e)
        else:
            return send_from_directory("./", "result.py", as_attachment=True)


def generateCode(data):
    l_graph = L_Graph()
    vertices = []
    for v in data:
        vertices.append(Vertex(str(v["id"]), v["type"]))
    for v in data:
        vFrom = next(filter(lambda x: x.name == str(v["id"]), vertices))
        for e in v["edges"]:
            vTo = next(filter(lambda x: x.name == str(e["to"]), vertices))
            vFrom.addEdge(Edge(vTo, e["input"], e["output"], e["bracket"]))
    for v in vertices:
        l_graph.addVertex(v)
    generator = CodeGenerator(l_graph)
    generator.generate()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
