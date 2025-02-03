# Chain request flow Async RPC example

This example has a minimal service oriented architecture for the purposes of demonstrating how Resonate acts as an async RPC framework.

When a cURL request is sent to the foo service, the `foo()` function sends a asynchronous RPC (known by Resonate as an RFI) to the `bar()` function on the bar service, which will cause the bar service to make an aynchronous RPC to the `baz()` function on the baz service.

The `foo()` function will wait for the result from `baz()` before returning.

## How to run the example

**Prerequisite**: This project uses [uv](https://docs.astral.sh/uv/) as the Python environment and package manager.

After cloning this repo, change directory into the root of the project and run the following command:

```shell
uv sync
```

You will need 4 separate terminal windows, one for each service and one to make the cURL request to the foo service.
Run the following commands, each in their own terminal:

_Terminal 1_

```shell
uv run foo
```

_Terminal 2_

```shell
uv run bar
```

_Terminal 3_

```shell
uv run baz
```

_Terminal 4_

Send a cURL request:

```shell
curl -X POST http://127.0.0.1:5000/foo
```

## Crash recovery exercise

In this exercise, you will see how Resonate's RFI is durable to process crashes.

First, modify the bar service by addomg a 10 second sleep to the bar function between the RFI call and the yielding of the promise.

```python
@resonate.register
def bar(ctx):
    try:
        print("running function bar")
        promise = yield ctx.rfi("baz").options(send_to=poll("service-baz"))
        yield ctx.sleep(10)
        result = yield promise
        return result + 1
    except Exception as e:
        print(e)
        raise
```

This will give you plenty of time to kill the process before the entire request flow completes.

Restart the bar service.

Now send a cURL request to the foo endpoint.

```shell
curl -X POST http://127.0.0.1:5000/foo
```

After you see the output `running function baz` from the baz service, kill the bar service.

Whenever you want, restart the bar service and you will see the request flow complete.
