from flask import Flask, Response
from omada import Omada  # ← correct class from omada wrapper
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/rss')
def rss_feed():
    ctrl = Omada(
        baseurl="https://your-controller-url",
        site="Default",
        username="admin",
        password="password",
        verify=False  # accept self-signed certs
    )
    ctrl.login()
    clients = ctrl.get_clients()

    fg = FeedGenerator()
    fg.title("Omada Connected Clients")
    fg.link(href="/rss")
    fg.description("Clients connected to your Omada Controller")

    for c in clients:
        fe = fg.add_entry()
        fe.id(c.get("mac", "") + str(c.get("hostname", "")))
        fe.title(c.get("hostname") or c.get("ip") or "Unknown")
        fe.description(f"IP: {c.get('ip')}, MAC: {c.get('mac')}")

    return Response(fg.rss_str(pretty=True), mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
