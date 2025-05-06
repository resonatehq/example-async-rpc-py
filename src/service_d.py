from resonate.message_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from threading import Event
import uuid


app_node_id = str(uuid.uuid4())
app_node_group = "service-d"

resonate = Resonate(
    store=RemoteStore(host="http://localhost", port="8001"),
    message_source=Poller(
        host="http://localhost", port="8002", id=app_node_id, group=app_node_group
    ),
)

@resonate.register
def qux(ctx, arg):
    print("running function qux")
    yield ctx.detached("quz", arg + 1).options(target="poll://service-e")


def main():
    resonate.start()
    print("service d is running")
    Event().wait()


if __name__ == "__main__":
    main()
