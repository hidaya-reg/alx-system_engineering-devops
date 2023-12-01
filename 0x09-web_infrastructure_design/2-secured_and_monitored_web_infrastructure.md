### Infrastructure Design:

#### 1. Components Added:
- **Three Firewalls**: Implemented to control incoming and outgoing network traffic, ensuring security by filtering and monitoring data.
- **SSL Certificate**: Used to encrypt traffic between the user's browser and the server for secure data transmission over HTTPS.
- **Monitoring Clients**: Three monitoring clients set up as data collectors (e.g., Sumo Logic) to monitor and gather data about system performance.

#### 2. Role of Additional Elements:
- **Firewalls**: Primarily added for security purposes, controlling traffic flow and protecting against unauthorized access or threats.
- **HTTPS Traffic**: Serves encrypted traffic to ensure data confidentiality, integrity, and authentication between the server and clients.
- **Monitoring**: Used for tracking system health, performance metrics, and identifying anomalies or issues proactively.
- **Monitoring Tool Data Collection**: Collects data through agents or data collectors installed on servers, collecting logs, metrics, and performance information.

#### 3. Monitoring for Web Server QPS:
- To monitor Web Server QPS (Queries per Second):
  - Set up monitoring tools to collect and analyze server logs and metrics.
  - Configure the monitoring tool to specifically track and report the number of queries or requests received by the web server per second.

### Issues with this Infrastructure:

#### 1. SSL Termination at Load Balancer Level:
- Terminating SSL at the load balancer exposes unencrypted traffic within the internal network, compromising security.

#### 2. Single MySQL Server Accepting Writes:
- Reliance on a single MySQL server capable of accepting writes poses a single point of failure risk, impacting availability if the server fails.

#### 3. Identical Server Components:
- Having identical server components (database, web server, application server) might lead to uniform vulnerabilities or limitations across all servers, increasing the risk if a specific vulnerability is exploited.

This infrastructure enhances security through firewalls and SSL, monitors system health, but faces issues with SSL termination, single points of failure in the MySQL setup, and potential uniform vulnerabilities across identical server components.

