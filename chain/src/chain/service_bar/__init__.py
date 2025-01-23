from resonate.task_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from resonate.targets import poll
from threading import Event

resonate = Resonate(
    store=RemoteStore(url="http://localhost:8001"),
    task_source=Poller(url="http://localhost:8002", group="service-bar"),
)


@resonate.register
def bar(ctx):
    try:
        print("running function bar")
        promise = yield ctx.rfc("baz").options(send_to=poll("service-baz"))
        # yield ctx.sleep(10)
        result = yield promise
        return result + 1
    except Exception as e:
        print(e)
        raise


def main():
    print("service bar is running")
    Event().wait()


if __name__ == "__main__":
    main()
