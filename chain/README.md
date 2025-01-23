# Chain request flow Async RPC example

This example has a minimal service oriented architecture for the purposes of demonstrating how Resonate acts as an async RPC framework.

When a cURL request is sent to the foo service, the `foo()` function sends a synchronous RPC (known by Resonate as an RFC) to the `bar()` function on the bar service, which will cause the bar service to make a synchronous RPC to the `baz()` function on the baz service.

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
