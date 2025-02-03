# Fire-and-forget request flow Async RPC example

**Note: Resonate's `detached()` API is still under development and currently only works with functions registered local to the call.**

## Running the project

This project uses [uv](https://docs.astral.sh/uv/) as the Python environment and package manager.

After cloning this repo, change directory into the root of the project and run the following command:

```shell
uv sync
```

You will need 2 separate terminal windows, one for the service and one to make the cURL request.
Run the following commands, each in their own terminal:

_Terminal 1_

```shell
uv run foo
```

_Terminal 2_

Send the cURL request:

```shell
curl -X POST http://127.0.0.1:5000/foo
```

_Abridged example code:_

`foo service`:

```python
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
```
