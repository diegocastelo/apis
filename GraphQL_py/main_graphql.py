from flask import Flask, request, jsonify
import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="Mundo"))

    def resolve_hello(self, info, name):
        return f"Olá, {name}!"


schema = graphene.Schema(query=Query)

app = Flask(__name__)


@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(debug=True)
