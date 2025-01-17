from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from threading import Event

resonate = Resonate(
    store=RemoteStore(url="http://localhost:8001"),
    task_source=Poller(url="http://localhost:8002", group="service-bar"),
)


@resonate.register
def bar(ctx):
    try:
        print("running function bar")
        return "Hello from bar!"
    except Exception as e:
        print(e)
        raise


def main():
    print("Service bar is running...")
    Event().wait()


if __name__ == "__main__":
    main()
