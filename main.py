import json
from session_manager import SessionManager

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    private_urls = config['private_urls']
    public_urls = config['public_urls']

    num_streams = int(input("Enter the number of streams to run: "))

    session_manager = SessionManager(private_urls, public_urls)
    session_manager.run_session(num_streams)

if __name__ == "__main__":
    main()