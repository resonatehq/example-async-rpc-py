from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from resonate.targets import poll
from flask import Flask, jsonify
import uuid


app = Flask(__name__)
resonate = Resonate()


def foo(ctx):
    try:
        print("running function foo")
        promise_id = str(uuid.uuid4())
        _ = yield ctx.detached(promise_id, bar, 1)
        return
    except Exception as e:
        print(e)
        raise


def bar(ctx, arg):
    try:
        print("running function bar")
        promise_id = str(uuid.uuid4())
        yield ctx.detached(promise_id, baz, arg + 1)
        return
    except Exception as e:
        print(e)
        raise


def baz(_, arg):
    try:
        print("running function baz")
        print(arg + 1)
        return
    except Exception as e:
        print(e)
        raise


resonate.register(foo)
resonate.register(bar)
resonate.register(baz)


@app.route("/foo", methods=["POST"])
def handle_foo():
    try:
        promise_id = str(uuid.uuid4())
        resonate.run(promise_id, foo)
        return jsonify({"message": "Detached request flow started"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def main():
    print("service foo is running")
    app.run(port=5000)


if __name__ == "__main__":
    main()
