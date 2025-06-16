from flask import Flask, Response
from omada.controller import OmadaController
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/rss')
def rss_feed():
    # Replace these with your actual controller details
    controller = OmadaController("https://your-controller-url", "admin", "password")
    controller.login()

    sites = controller.get_sites()

    fg = FeedGenerator()
    fg.title("Omada Sites Feed")
    fg.link(href="http://example.com/rss")
    fg.description("Status updates from Omada")

    for site in sites:
        fe = fg.add_entry()
        fe.title(f"Site: {site['name']}")
        fe.link(href="http://example.com/site/" + site['id'])
        fe.description(str(site))

    return Response(fg.rss_str(), mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

