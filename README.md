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

In terminal 4, send cURL requests with a behavior flag.

The two types of behavior are:

- `chain`: The `chain` flag will cause the foo service to make an synchronous RPC to the bar service, which will cause the bar service to make a synchronous RPC to the baz service.

- `fan`: The `fan` flag will cause the foo service to make two asynchronous RPCs, one to the bar service and one to the baz service, and await on the results only after making the RPCs.

Example cURL request:

```shell
curl -X POST http://127.0.0.1:5000/foo -H "Content-Type: application/json" -d '{"behavior": "chain"}'
```
