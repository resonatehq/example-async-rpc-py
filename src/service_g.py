from resonate.message_sources.poller import Poller
from resonate.stores.remote import RemoteStore
from resonate import Resonate
from threading import Event
import uuid


app_node_id = str(uuid.uuid4())
app_node_group = "service-g"

resonate = Resonate(
    store=RemoteStore(host="http://localhost", port="8001"),
    message_source=Poller(
        host="http://localhost",
        port="8002",
        id=app_node_id,
        group=app_node_group,
    ),
)


@resonate.register
def zim(ctx, arg):
    print("running function zim")
    promise_bar = yield ctx.rfi("rax").options(target="poll://service-h")
    promise_baz = yield ctx.rfi("dop").options(target="poll://service-i")
    result_bar = yield promise_bar
    result_baz = yield promise_baz
    return result_bar + result_baz + arg


def main():
    resonate.start()
    print(f"app node id {app_node_id} | app node group {app_node_group} | running")
    Event().wait()


if __name__ == "__main__":
    main()
