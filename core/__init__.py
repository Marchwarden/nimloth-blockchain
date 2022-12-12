from flask import Flask, request, url_for, redirect, render_template
from .blockchain import Blockchain
from .block import NimlothBlock
from .transaction import Transaction


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    block_chain = Blockchain([], [], 2)
    current_block = NimlothBlock("null", block_chain.printhash(), 0.0, 0, [])
    new_transaction = Transaction("null", "null", 0, "null")
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route("/")
    def init():
        return redirect(url_for("home"))

    @app.route("/success/<name>")
    def success(name):
        return "welcome"

    @app.route("/home", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            if request.form["submit_button"] == "add_current_block":
                proof = current_block.hash = block_chain.proof_of_work(current_block)
                block_chain.add_block(current_block, proof)
                current_block.clearblock()
            elif request.form["submit_button"] == "add_transaction":
                sender = request.form["sender"]
                reciever = request.form["reciever"]
                amount = request.form["amount"]
                coin = request.form["coin"]

                if isinstance(amount, float) is not True:
                    return render_template(
                        "home.html",
                        block_chain=block_chain,
                        current_block=current_block,
                    )

                new_transaction = Transaction(sender, reciever, amount, coin)
                block_chain.add_new_transaction(new_transaction)
                action = "add transaction"
                return render_template(
                    "home.html",
                    block_chain=block_chain,
                    current_block=current_block,
                    new_transaction=new_transaction,
                )

        blockchain = request.args.get("blockchain")
        return render_template(
            "home.html", block_chain=block_chain, current_block=current_block
        )

    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            user = request.form["name"]
            return redirect(url_for("success", name=user))
        user = request.args.get("name")
        return render_template("login.html")

    @app.route("/display/")
    def display():
        return render_template("display.html")

    return app
