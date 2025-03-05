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
def foo(ctx):
    try:
        print("running function foo")
        promise_bar = yield ctx.rfi("bar").options(send_to=poll("service-bar"))
        promise_baz = yield ctx.rfi("baz").options(send_to=poll("service-baz"))
        result_bar = yield promise_bar
        result_baz = yield promise_baz
        return result_bar + result_baz + 1
    except Exception as e:
        print(e)
        raise


@app.route("/foo", methods=["POST"])
def handle_foo():
    try:
        promise_id = str(uuid.uuid4())
        handle = foo.run(promise_id)
        result = handle.result()
        return jsonify({"message": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main():
    print("service foo is running")
    app.run(port=5000)


if __name__ == "__main__":
    main()
