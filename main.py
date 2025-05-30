import wifi
import socketpool
import time
import storage
from adafruit_wsgi.wsgi_app import WSGIApp
import wsgiserver as server

# Set access point credentials
ap_ssid = "myAP"
ap_password = "password123"

# Configure access point
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

# Print access point settings
print("Access point created with SSID: {} and password: {}".format(ap_ssid, ap_password))
print("My IP address is:", str(wifi.radio.ipv4_address_ap))

# Create WSGI application
web_app = WSGIApp()

# Define the Hello World route
@web_app.route("/")
def hello_world(request):
    response = (
        "<!DOCTYPE html>"
        "<html>"
        "<head><title>Hello World</title></head>"
        "<body><h1>Hello, World!</h1></body>"
        "</html>"
    )
    return ("200 OK", [("Content-Type", "text/html")], response)

# Start the web server
def start_web_service():
    HOST = str(wifi.radio.ipv4_address_ap)
    PORT = 80
    print(f"Open this IP in your browser: http://{HOST}:{PORT}/")

    # Start the WSGI server
    wsgi_server = server.WSGIServer(PORT, application=web_app)
    wsgi_server.start()

    try:
        while True:
            wsgi_server.update_poll()
            time.sleep(0.1)  # Poll every 100ms
    except KeyboardInterrupt:
        print("Stopping server...")
        wsgi_server.stop()

# Run the web service
start_web_service()
