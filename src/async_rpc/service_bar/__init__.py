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
def bar(ctx, behavior):
    try:
        print("running function bar")
        if(behavior == "chain"):
            print("behavior = chain, making a sync call to baz...")
            result = yield ctx.rfc("baz").options(send_to=poll("service-baz"))
            print(result)
            return f"{result} & Hello from bar!"
        elif(behavior == "fan"):
            print("behavior = fan, returning...")
            return "Hello from bar!"
        else:
            raise Exception("Invalid behavior")
    except Exception as e:
        print(e)
        raise

def main():
    print("Service bar is running...")
    Event().wait()


if __name__ == "__main__":
    main()
