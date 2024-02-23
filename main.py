from flask import Flask, request
from flask_cors import CORS
import sqlite3
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text



model = tf.keras.models.load_model('bert_model.h5',{"KerasLayer":hub.KerasLayer},compile=False)
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
connection = sqlite3.connect('database.db')

app = Flask(__name__)
CORS(app)

@app.get("/comments")
def comment_get():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = 'select * from comments'
    result = cursor.execute(query)
    res = result.fetchall()
    key = ["commentBody"] * len(res)
    ans = [dict(zip(key,row)) for row in res]
    connection.close()
    return ans

@app.post("/comments")
def comment_post():
    data = request.get_json(silent=True)
    text = data["commentBody"]
    ans = model.predict([text])
    ans = ans[0]
    print(ans)
    if(ans >= 0.5):
        return {"status": False}
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = 'insert into comments values ("'+text+'")'
    cursor.execute(query)
    connection.commit()
    connection.close()
    return {"status":True}

if __name__ == '__main__':
    app.run(debug=True, port=3001)