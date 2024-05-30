from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    # URL of the radio stream (input via query parameter 'url')
    radio_url = request.args.get('url')
    if not radio_url:
        return "Error: No URL provided", 400

    # Fetch the radio stream data
    try:
        stream = requests.get(radio_url, stream=True)
    except requests.RequestException as e:
        return f"Error fetching stream: {e}", 500

    # Stream the data to the client
    def generate():
        for chunk in stream.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    return Response(generate(), content_type=stream.headers['content-type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
