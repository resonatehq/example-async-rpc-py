# Async RPC | Resonate example application

This example application showcases Resonate's Async RPC capabilities with three different request flows.

- [await chain](./await_chain/README.md)
- [detached chain](./detached_chain/README.md)
- [fan out workflow](./fan_out_workflow/README.md)

To learn more about Resonate as an Async RPC, checkout the [Resonate is also an Async RPC Framework](https://resonatehqio.substack.com/p/resonate-is-also-an-async-rpc-framework) article.

## Project prerequisites

This example application uses [uv](https://docs.astral.sh/uv/) as the Python environment and package manager.

After cloning this repo, change directory into the root of the project and run the following command to install dependencies:

```shell
uv sync
```

This example application requires that a [Resonate Server](https://docs.resonatehq.io/get-started/server-quickstart) is running locally.

# Resonate's remote invocations

Resonate offers several APIs to invoke a function that is remote to the calling process.

## Ephemeral to Durable

## Durable

Resonate API surface
RPC = Remote Procedure Call
RFI = stands for Remote Function Invocation.

With Resonate a Remote Function Invocation returns a Durable Promise. You don't have to block the rest of the function on the result of the function that was invoked. You can yield the result at any point later in the execution. However, yielding the result of the promise (yielding the result of the function that was invoked) does block execution until the result is available. In other words, RFI is an asynchronous API.

RFC stands for Remote Function Call, it is effectively an RFI but with syntax sugar, and yields the result of the function that was invoked. In other words, it is a synchronous API.

# initialize Resonate

# this instance uses a Resonate Server for remote promise and task storage

# this instance uses a poller to receive messages (polls the server for messages)

    # id and group enable unicast and anycast
    # id is the unique identifier for this instance
    # group is the group name for this instance


    # do not try/except here
    # if this function throws an exception,
    # it's caught by Resonate and automatically retried

route handler

# create a unique promise id

        # invoke foo with the promise id
        # .rpc invokes foo at the target

## Await Chain request flow

The Await Chain request flow is one where there is a synchronous chain of calls starting from the cURL request sent in the terminal, then through the HTTP gateway, service a, service b, and finally service c.

![Await Chain request flow diagram](./static/await-chain-flow.png)

Resonate is used in the HTTP gateway to transition the request flow from an ephemeral request flow into a durable one.

This request flow is synchronous — that is, the curl request is blocked waiting on the result from the full chain of calls that goes down to `bar()` and propagates back up. The process that made the cURL request prints the result.

### How to run the Await Chain example

You'll need 5 separate terminal windows (not including the one running the Resonate Server), one for each service and one to make the cURL request to the gateway.

Run the following commands, each in their own terminal:

_Terminal 1_

```shell
uv run gateway
```

_Terminal 2_

```shell
uv run a
```

_Terminal 3_

```shell
uv run b
```

_Terminal 4_

```shell
uv run c
```

_Terminal 5_

Send a cURL request:

```shell
curl -X POST http://127.0.0.1:5000/await-chain
```

## Detached Chain request flow

The Detached Chain is one where each function plays a role, passing off a result to the next function without waiting on the child invocations.

![Detached Chain request flow diagram](./static/detached-chain-flow.png)

Resonate transitions the request in the route handler from an ephemeral call to a durable one.

However, unlike the Await Chain flow, the each function returns once it has invoked the next function. There is no waiting on the result, and the last function in the chain prints the result.

### How to run the Detached Chain example

You will need 5 separate terminal windows (not including the one running the Resonate Server), one for each service and one to make the cURL request (assuming you don't already have the gateway running or a process for the cURL request from the previous example).

Run the following commands, each in their own terminal:

_Terminal 1_

```shell
uv run gateway
```

_Terminal 2_

```shell
uv run d
```

_Terminal 3_

```shell
uv run e
```

_Terminal 4_

```shell
uv run f
```

_Terminal 5_

Send the cURL request:

```shell
curl -X POST http://127.0.0.1:5000/detached-chain
```

## Fan-out Workflow request flow

The Fan-out Workflow request is one where multiple functions are invoked from a caller function, and the result of each of the invoked functions is combined inside the caller to produce the result.

![Fan-Out Workflow request flow diagram](./static/fan-out-workflow-flow.png)

Resonate transitions the request from ephemeral to durable at the route handler.

The `zim()` function then acts as a workflow, invoking `rax()` and `dop()` asynchronously, that is — receiving promises at their invocation and awaiting on the results via the promises later on.

The `zim()` function combines the results of the steps and returns it to the caller where the result is printed.

## How to run the Fan-out Workflow example

You will need 5 separate terminal windows (not including the one running the Resonate Server), one for each service and one to make the cURL request (assuming you don't already have the gateway running or a process for the cURL request from the previous example).

Run the following commands, each in their own terminal:

_Terminal 1_

```shell
uv run gateway
```

_Terminal 2_

```shell
uv run g
```

_Terminal 3_

```shell
uv run h
```

_Terminal 4_

```shell
uv run i
```

_Terminal 5_

```shell
uv run h
```

Example cURL request:

```shell
curl -X POST http://127.0.0.1:5000/fan-out-workflow
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
