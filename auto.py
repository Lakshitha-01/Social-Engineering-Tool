import subprocess
import requests
import time

def start_ngrok(port=5000):
    # Start ngrok tunnel
    ngrok = subprocess.Popen(['ngrok', 'http', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Wait for ngrok to initialize
    time.sleep(2)

    try:
        # Query the local ngrok API for tunnel info
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        tunnels = response.json()['tunnels']

        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                public_url = tunnel['public_url']
                print(f"ngrok tunnel is live at: {public_url}")
                return public_url
    except Exception as e:
        print("Error getting ngrok URL:", e)
        return None

# Example usage
if __name__ == "__main__":
    url = start_ngrok(5000)
