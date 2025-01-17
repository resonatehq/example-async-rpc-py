from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from resonate.targets import poll
from flask import Flask, jsonify
import uuid


app = Flask(__name__)
resonate = Resonate(
    store=RemoteStore(url="http://localhost:8001"),
    task_source=Poller(url="http://localhost:8002", group="service-foo"),
)


@resonate.register
def foo_rfi(ctx):
    try:
        print("running function foo_rfi")
        promise = yield ctx.rfi("bar").options(send_to=poll("service-bar"))
        result = yield promise
        return result
    except Exception as e:
        print(e)
        raise


@resonate.register
def foo_rfc(ctx):
    try:
        print("running function foo_rfc")
        result = yield ctx.rfc("bar").options(send_to=poll("service-bar"))
        return result
    except Exception as e:
        print(e)
        raise


@app.route("/foo_rfi", methods=["GET"])
def handle_foo_rfi():
    try:
        promise_id = str(uuid.uuid4())
        handle = foo_rfi.run(promise_id)
        message = handle.result()
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/foo_rfc", methods=["GET"])
def handle_foo_rfc():
    try:
        promise_id = str(uuid.uuid4())
        handle = foo_rfc.run(promise_id)
        message = handle.result()
        return jsonify({"message": message}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main():
    print("Service foo is running...")
    app.run(port=5000)


if __name__ == "__main__":
    main()
