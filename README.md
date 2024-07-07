# ft_transcendence

[日本語版はこちら](./docs/README_ja.md)

## Overview

ft_transcendence is a web application project developed as the final assignment for 42. This project uses Django as the backend, with HTML, CSS, JavaScript, and Bootstrap for the frontend. It implements real-time Ping Pong game matches and real-time chat functionality using socket communication.

Additionally, Grafana and Prometheus are integrated using Docker, allowing for server state monitoring.

## Key Features

1. **Ping Pong Game**:

   - A game where players compete for points using two paddles and one ball
   - Remote play functionality
   - Tournament mode

2. **Real-time Chat**:

   - Private chat between individuals
   - Real-time message sending and receiving
   - Ability to invite chat partners to a game using the `:invite` command

3. **Server Monitoring**:
   - Server state visualization using Grafana and Prometheus

## Setup Instructions

### Prerequisites

- An environment capable of running Docker

### Installation

1. Clone the repository:

   ```
   git clone [repository URL]
   cd ft_transcendence
   ```

2. Copy the environment variable file:

   ```
   cp .env.example .env
   ```

3. Start the Docker containers:
   ```
   sudo make up-d
   ```

This will start the following services in the background:

- web-prod (for product deployment)
- web-dev (development environment)
- web-db (database)
- grafana
- prometheus

### How to Access

- Web application: `https://localhost:8000`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

Note: For detailed configuration and usage of Grafana and Prometheus, please refer to [MONITOR_README.md](./docs/MONITOR_README.md).

## Development Environment

To run the project in a development environment:

1. Enter the development container:

   ```
   sudo make exec web-dev
   ```

2. Generate an SSL certificate:

   ```
   openssl req -x509 -newkey rsa:4096 -keyout "$KEY_PATH" -out "$CERT_PATH" -days 365 -nodes -subj "/CN=localhost"
   ```

3. Start the development server:

   ```
   daphne --settings=PongChat.settings PongChat.asgi:application
   ```

4. Access `https://localhost:8001` to start development.

Note: If you make changes to files, please restart the server to reflect the changes.

## Directory Structure

```
.
├── PongChat
│   ├── PongChat
│   ├── accounts
│   ├── chat
│   ├── locale
│   ├── media
│   ├── pingpong
│   ├── static
│   └── templates
├── data
├── docs
├── node_modules
├── sample_code
├── tests
└── tools
    └── docker
        ├── web_dev
        └── web_prod
```

## Technologies Used

- Backend: Django 5.0.4
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: PostgreSQL
- Real-time Communication: Django Channels
- Containerization: Docker
- Monitoring: Grafana, Prometheus

For other dependencies, please refer to [requirements.txt](./requirements.txt).

## Contributing

If you have any issues or suggestions, please create an Issue.

## Contributers
<a href="https://github.com/yuki-shimoda-crypto/42_ft_transcendence/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yuki-shimoda-crypto/42_ft_transcendence" />
</a>

## License

This project is released under the [MIT License](LICENSE).

## Contact

Currently, there is no specific contact information. If you have any questions or concerns, please reach out through GitHub Issues.
