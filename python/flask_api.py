from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

import npcGenerator
import npcInfoGenerator

app = Flask(__name__)
api = Api(app)


class NPC(Resource):
    def get(self):
        getResponse = {}
        npcInfo = npcInfoGenerator.npcInfoGenerator()
        # getResponse = jsonify(npcGenerator.npcGenerator())
        # getResponse.status_code = 200
        npcInfo.generateInfo()
        getResponse = jsonify(npcInfo.npcPrintInfo())

        return getResponse


api.add_resource(NPC, '/npcGen')

if __name__ == "__main__":
    app.run(debug=True)
