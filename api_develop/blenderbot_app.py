from flask import Flask, request, jsonify
from utils import blender_bot_answer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello world!"

@app.route("/blender-bot", methods=["POST"])
def interact():
   try:
        message = request.get_json().get('message')
    
    
        answer = blender_bot_answer(message)
        
        special_tokens = ["<pad>",
                            "<s>",
                            "</s>",
                            "</S>",
                            "<S>",
                            "<unk>",
                            "<mask>",
                             "<UNK>",
                             "<PAD>",
                             "<MASK>"
                            ]
        for token in special_tokens:
            answer = answer.replace(token, "")
        
        if not message:
            jsonify({
                "code": 200,
                "message": "Bạn phải nhập vào gì đó chứ ^-^"
            })
        
        return jsonify({
            "code": 200,
            "message": answer
        })
   except Exception as e:
       return jsonify({
           "message": str(e) or "Xảy ra lỗi!"
       })

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=True)