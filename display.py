from flask import Flask, jsonify, request

app = Flask(__name__)

@app.before_request
def check_old_db_access():
    # Check if the request is trying to access the old database
    if "old_database_route" in request.path:
        return jsonify({"message": "This database is no longer in use."}), 403

@app.route("/old_database_route")
def old_database_route():
    # Example route that would trigger the deprecation message
    pass

@app.route("/")
def home():
    return "Welcome to the new database!"

if __name__ == "__main__":
    app.run(debug=True)
