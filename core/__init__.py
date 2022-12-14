import json
import os
from flask import Flask, request, url_for, redirect, render_template
from .block_files.blockchain import Blockchain
from .block_files.block import NimlothBlock
from .io_helpers import blockchain_io


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    block_chain = Blockchain([], [], 2)
    current_block = NimlothBlock(0, "null", block_chain.get_previous_hash(), 0.0, 0, [])
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

    @app.route("/save", methods=["POST", "GET"])
    def save():
        document_path = os.getcwd() + "/core/json/blocktest.txt"
        with open(document_path, "wb") as file_handle:
            file_handle.write(block_chain._to_json().encode("utf-8"))
        # filef = open(document_path, "wb")
        # filef.write(block_chain._to_json().encode("utf-8"))
        return "blockchain saved"

    @app.route("/dev/add", methods=["POST", "GET"])
    def dev_add():
        if request.method == "POST":
            new_hash = request.args.get("hash")
            block_chain.add_block_dev(new_hash)
        return render_template("add.html", block_chain=block_chain)

    @app.route("/home", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            if request.form["submit_button"] == "add_current_block":
                proof = current_block.hash = block_chain.proof_of_work(current_block)
                block_chain.add_block(current_block, proof)
                current_block.clearblock()
            elif request.form["submit_button"] == "add_transaction":
                action = "add transaction"
        blockchain = request.args.get("blockchain")
        return render_template(
            "home.html", block_chain=block_chain, current_block=current_block
        )

    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            block_chain.add_block_dev(3)
        user = request.args.get("name")
        return render_template("login.html", block_chain=block_chain)

    return app
