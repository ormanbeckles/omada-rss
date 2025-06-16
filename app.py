from flask import Flask, Response
from omada import Omada  # ← Import the correct wrapper class
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/rss')
def rss_feed():
    # Replace with real controller info
    controller = Omada(
        base_url="https://your-controller-url",  # no trailing slash
        username="admin",
        password="password",
        site="Default"  # Or the actual site ID if you know it
    )
    controller.login()

    clients = controller.get_clients()

    fg = FeedGenerator()
    fg.title("Omada Connected Clients")
    fg.link(href="http://example.com/rss")
    fg.description("RSS feed of connected clients")

    for client in clients:
        fe = fg.add_entry()
        fe.title(client.get("name", "Unnamed Device"))
        fe.link(href=f"http://example.com/client/{client.get('mac', '')}")
        fe.description(str(client))

    return Response(fg.rss_str(), mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
