# Resonate is also an async RPC framework

This example has a minimal service oriented architecture for the purposes of demonstrating how Resonate acts as an async RPC framework.

When a cURL request is sent to the foo service, the `foo()` function sends two asynchronous RPCs (known by Resonate as RFIs)

- 1 to the `bar()` function and sends a on the bar service.
- 1 to the `baz()` function on the baz service.

The `foo()` function will then yield the result of the promises from both invocations before returning.

## Running the project

This project uses [uv](https://docs.astral.sh/uv/) as the Python environment and package manager.

After cloning this repo, change directory into the root of the project and run the following command:

```shell
uv sync
```

You will need 4 separate terminal windows, one for each service and one to make the cURL request.
Run the following commands, each in their own terminal:

Terminal 1

```shell
uv run foo
```

Terminal 2

```shell
uv run bar
```

Terminal 3

```shell
uv run baz
```

In terminal 4, send cURL requests with a behavior flag.

Example cURL request:

```shell
curl -X POST http://127.0.0.1:5000/foo
```

_Abridged example code:_

```python
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

```
