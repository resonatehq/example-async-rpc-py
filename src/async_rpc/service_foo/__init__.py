from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from resonate.targets import poll
from flask import Flask, jsonify, request
import uuid


app = Flask(__name__)
resonate = Resonate(
    store=RemoteStore(url="http://localhost:8001"),
    task_source=Poller(url="http://localhost:8002", group="service-foo"),
)


@resonate.register
def foo(ctx, behavior):
    try:
        print("running function foo")
        if behavior == "chain":
            print("behavior = chain, making a sync call to bar...")
            result = yield ctx.rfc("bar", behavior).options(send_to=poll("service-bar"))
            print(result)
            return f"{result} & Hello from foo!"
        elif behavior == "fan":
            print("behavior = fan, making async calls to bar and baz...")
            promise_bar = yield ctx.rfi("bar", behavior).options(send_to=poll("service-bar"))
            promise_baz = yield ctx.rfi("baz").options(send_to=poll("service-baz"))
            result_bar = yield promise_bar
            print(result_bar)
            result_baz = yield promise_baz
            print(result_baz)
            return f"{result_bar} & {result_baz} & Hello from foo!"
        else:
            raise Exception("Invalid behavior")
    except Exception as e:
        print(e)
        raise


@app.route("/foo", methods=["POST"])
def handle_foo():
    try:
        data = request.get_json()
        behavior = data["behavior"]
        promise_id = str(uuid.uuid4())
        handle = foo.run(promise_id, behavior)
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
