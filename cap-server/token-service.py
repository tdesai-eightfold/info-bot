import os
from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

load_dotenv('.env.local')  # Mistake-1

app = Flask(__name__)
CORS(app, origins="*")

api_rest = Api(app, title="LiveKit Token Service", version="1.0")
ns = api_rest.namespace("api")

@ns.route("/token")
class TokenResource(Resource):
    def get(self):
        room = request.args.get("room")
        identity = request.args.get("identity", "frontend-user")

        if not room:
            return {"error": "room query parameter is required"}, 400

        # 🔍 sanity check (remove later)
        assert os.getenv("LIVEKIT_API_KEY"), "LIVEKIT_API_KEY missing"
        assert os.getenv("LIVEKIT_API_SECRET"), "LIVEKIT_API_SECRET missing"

        token = (
            api.AccessToken(
                os.getenv("LIVEKIT_API_KEY"),
                os.getenv("LIVEKIT_API_SECRET"),
            )
            .with_identity(identity)
            .with_grants(
                api.VideoGrants(
                    room=room,
                    room_join=True,
                    can_publish=True,
                    can_subscribe=True,
                    can_publish_data=True,  # Mistake-2
                )
            )
            .to_jwt()
        )

        return {"token": token}, 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
