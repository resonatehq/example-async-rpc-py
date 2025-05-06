from resonate.message_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate.resonate import Resonate
from threading import Event
import uuid


app_node_id = str(uuid.uuid4())
app_node_group = "service-c"

resonate = Resonate(
    store=RemoteStore(host="http://localhost", port="8001"),
    message_source=Poller(
        host="http://localhost", port="8002", id=app_node_id, group=app_node_group
    ),
)


@resonate.register
def baz(_):
    print("running function baz")
    return 1


def main():
    resonate.start()
    print(f"app node id {app_node_id} | app node group {app_node_group} | running")
    Event().wait()


if __name__ == "__main__":
    main()
