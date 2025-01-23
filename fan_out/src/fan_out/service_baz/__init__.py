from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from threading import Event

resonate = Resonate(
    store=RemoteStore(url="http://localhost:8001"),
    task_source=Poller(url="http://localhost:8002", group="service-baz"),
)


@resonate.register
def baz(_):
    try:
        print("running function baz")
        return 1
    except Exception as e:
        print(e)
        raise


def main():
    print("Service baz is running...")
    Event().wait()


if __name__ == "__main__":
    main()
