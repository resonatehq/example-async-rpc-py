# Resonate is also an async RPC framework

This project has a minimal service oriented architecture for the purposes of demonstrating how Resonate acts as an async RPC framework.

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
curl -X POST http://127.0.0.1:5000/foo -H "Content-Type: application/json" -d '{"behavior": "chain"}'
```

The two types of behavior are:

- `chain`: The `chain` flag will cause the foo service to make an synchronous RPC (known by Resonate as an RFC) to the bar service, which will cause the bar service to make a synchronous RPC to the baz service.

_Abridged example code:_

`foo service`:

```python
def foo():
    result = yield ctx.rfc("bar", behavior).options(send_to=poll("service-bar"))
    return f"{result} & Hello from foo!"
```

`bar service`:

```python
def bar():
    result = yield ctx.rfc("baz").options(send_to=poll("service-baz"))
    return f"{result} & Hello from bar!"
```

`baz service`:

```python
def baz():
    yield ctx.sleep(5)
    return "Hello from baz!"
```

- `fan`: The `fan` flag will cause the foo service to make two asynchronous RPCs (known by Resonate as RFIs), one to the bar service and one to the baz service, and await on the results only after making the RPCs.

_Abridged example code:_

`foo service`:

```python
def foo():
    promise_bar = yield ctx.rfi("bar", behavior).options(send_to=poll("service-bar"))
    promise_baz = yield ctx.rfi("baz").options(send_to=poll("service-baz"))
    result_bar = yield promise_bar
    result_baz = yield promise_baz
    return f"{result_bar} & {result_baz} & Hello from foo!"
```

`bar service`:

```python
def bar():
    return "Hello from bar!"
```

`baz service`:

```python
def baz():
    yield ctx.sleep(5)
    return "Hello from baz!"
```

## RFCs vs RFIs

RFI stands for Remote Function Invocation.

With Resonate a Remote Function Invocation returns a Durable Promise. You don't have to block the rest of the function on the result of the function that was invoked. You can yield the result at any point later in the execution. However, yielding the result of the promise (yielding the result of the function that was invoked) does block execution until the result is available. In other words, RFI is an asynchronous API.

RFC stands for Remote Function Call, it is effectively an RFI but with syntax sugar, and yields the result of the function that was invoked. In other words, it is a synchronous API.
