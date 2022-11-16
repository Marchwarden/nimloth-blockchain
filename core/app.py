from flask import Flask
from blockchain import Blockchain

app = Flask(__name__)

# Generate a globally unique address for this node


# Instantiate the Blockchain
blockchain = Blockchain()

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    args = parser.parse_args()
    port = args.port

    app.run(host="0.0.0.0", port=port)


@app.route("/")
def main():
    return "Hello"
