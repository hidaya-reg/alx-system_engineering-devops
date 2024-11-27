# 0x09. Web infrastructure design
## Resources
- [What is a database](https://www.oracle.com/ke/database/what-is-database/)
- [What’s the difference between a web server and an app server?](https://www.infoworld.com/article/2171154/app-server-web-server-what-s-the-difference.html)
- [DNS record types](https://www.site24x7.com/learn/dns-record-types.html)
- [How to avoid downtime when deploying new code](https://softwareengineering.stackexchange.com/questions/35063/how-do-you-update-your-production-codebase-database-schema-without-causing-downt#answers-header)
- [High availability cluster (active-active/active-passive)](https://docs.oracle.com/cd/E17904_01/core.1111/e10106/intro.htm#ASHIA712)
- [What is HTTPS](https://www.instantssl.com/http-vs-https)
- [What is a firewall](https://www.webopedia.com/definitions/firewall/)

## Learning Objectives
<details>
<summary>LAMP, SPOF, QPS</summary>

- **LAMP:** A common open-source web development stack. It stands for:
    + Linux: The operating system.
    + Apache: The web server.
    + MySQL: The database management system.
    + PHP (or sometimes Python or Perl): The programming language.
    + This stack is widely used for developing dynamic websites and applications.

- **SPOF (Single Point of Failure):** In a system or architecture, an SPOF is any individual component whose failure would cause the entire system to stop working. Reducing SPOFs is critical for high availability and reliability. Techniques to mitigate SPOFs include redundancy, load balancing, and failover systems.

- **QPS (Queries Per Second):** A measure of the number of queries a system can handle per second. It’s used to evaluate the performance and scalability of databases, search engines, and other systems that handle a large number of requests.
</details>
<details>
<summary>What's a web server</summary>

### Web Server
A web server is a software or hardware system that serves HTTP content to clients, typically browsers, over the internet or a private network. Its main job is to process requests for web pages and resources and send the requested content back to the client. Web servers are often the first layer in web application architecture, receiving incoming requests and either serving static files (e.g., HTML, CSS, images) or routing requests to other servers, like an application server, for more complex processing.

#### Key Functions of a Web Server
- **Handling HTTP Requests:** Accepts HTTP requests, typically from a browser, for files or other resources.
- **Serving Static Content:** Delivers static files like HTML, CSS, JavaScript, and images directly to the client.
- **Routing Dynamic Requests:** When a request requires dynamic data or server-side processing (e.g., fetching data from a database), the web server can route the request to an application server (e.g., Python application with Flask or Django) and then serve the response back to the client.
- **Load Balancing:** Distributes traffic across multiple servers to ensure the system is scalable and resilient.
- **Security and SSL Handling:** Implements HTTPS by managing SSL/TLS encryption, which helps secure data during transit.

#### Example: Nginx as a Web Server with Python (Using WSGI)
Nginx is a high-performance web server known for its ability to handle a large number of concurrent connections. It’s widely used for serving static content, load balancing, and acting as a reverse proxy. When using Nginx with Python, Nginx often acts as a reverse proxy in front of a Python application, allowing Nginx to serve static content directly and route dynamic requests to the Python app.

Here’s how this setup might look:

#### 1. Install Nginx and Python Application (e.g., Flask)
Install Nginx and set up your Python web application (in this case, a simple Flask app).
```bash
# Install Nginx
sudo apt update
sudo apt install nginx

# Install Flask and a WSGI server (e.g., Gunicorn)
pip install flask gunicorn
```
#### 2. Create a Simple Python Web Application (Flask)
Create a Python script named app.py using Flask.

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello from Flask with Nginx!")

if __name__ == '__main__':
    app.run()
```
#### 3. Run the Application with Gunicorn (WSGI Server)
Gunicorn is a WSGI (Web Server Gateway Interface) server, which enables Nginx to communicate with your Python application.

```bash
# Run Gunicorn to serve the Flask app
gunicorn --bind 127.0.0.1:8000 app:app
```
This command binds Gunicorn to listen on `127.0.0.1:8000` and serve the `app` module.

#### 4. Configure Nginx as a Reverse Proxy to Gunicorn
Configure Nginx to forward incoming requests to Gunicorn, so it can process the Python application.

- Create a new configuration file for your site in `/etc/nginx/sites-available/`:

```bash
sudo nano /etc/nginx/sites-available/my_flask_app
```
- Add the following configuration to route traffic through Nginx to Gunicorn:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- Enable the configuration by creating a symbolic link to the sites-enabled directory:

```bash
sudo ln -s /etc/nginx/sites-available/my_flask_app /etc/nginx/sites-enabled
```
- Test the Nginx configuration for syntax errors and reload it:

```bash
sudo nginx -t
sudo systemctl restart nginx
```
#### 5. Accessing the Application
Now, when you access `http://your_domain_or_ip`, Nginx receives the request, and if it’s a static request, it serves it directly. For dynamic requests (like `/`), it forwards the request to Gunicorn, which runs the Flask app and sends the response back to Nginx. Nginx then returns this response to the client.

#### Why Use Nginx with Python?
Using Nginx in front of a Python application provides several benefits:

- **Improved Performance:** Nginx handles static content efficiently and manages a large number of connections, reducing the load on the Python app.
- **Load Balancing:** Nginx can distribute incoming traffic across multiple instances of the Python app.
- **SSL Termination:** Nginx manages SSL certificates, handling encryption/decryption to offload the task from the Python app.
- **Security:** Nginx provides an additional security layer, filtering requests before they reach the application.

</details>
<details>
<summary>what is reverse proxy</summary>

### Reverse Proxy
A reverse proxy is a type of server that sits between client devices (like browsers) and backend servers, forwarding client requests to the appropriate server and then sending the server's response back to the client. Unlike a regular proxy (or "forward proxy"), which typically hides the client’s identity from the server, a reverse proxy sits in front of the server and often hides the server's identity from the client.

#### Key Purposes and Benefits of a Reverse Proxy
- **Load Balancing:** Distributes client requests across multiple backend servers to ensure no single server is overloaded. This improves performance and allows the system to scale.

- **SSL Termination:** Handles SSL encryption and decryption on behalf of backend servers. This offloads SSL processing from application servers, improving their performance and simplifying certificate management.

- **Caching:** Stores copies of frequently requested content, which reduces the load on backend servers and speeds up responses for clients. Commonly cached items include static assets like images, CSS, or JavaScript files.

- **Security:** Acts as a barrier between clients and backend servers, masking server details (such as IP addresses and server types). A reverse proxy can also block suspicious requests, protecting backend servers from attacks like Distributed Denial of Service (DDoS).

- **Compression:** Compresses server responses before sending them to clients, reducing bandwidth usage and speeding up loading times for clients.

- **Centralized Authentication and Authorization:** Enforces authentication and authorization policies before requests reach backend servers, adding another layer of security.

#### How a Reverse Proxy Works
1. **Client Request:** A client, like a browser, makes a request to a website or web application.
2. **Reverse Proxy Receives Request:** The request goes to the reverse proxy (e.g., Nginx or Apache), rather than directly to the backend servers.
3. **Request Handling:** The reverse proxy decides what to do with the request. It might:
- Forward the request to an appropriate backend server (load balancing).
- Serve a cached version if the content is available.
- Terminate SSL and forward the request in plaintext to the backend.
4. **Response:** The backend server processes the request and sends the response back to the reverse proxy.
5. **Client Response:** The reverse proxy forwards the response to the client, often hiding the backend server details.

#### Example of a Reverse Proxy with Nginx and a Python Application
In a typical setup, Nginx can be configured as a reverse proxy in front of a Python application (e.g., a Flask or Django app served with Gunicorn). Here’s how it works:
1. Nginx, the reverse proxy, receives requests from clients on port 80 (HTTP) or 443 (HTTPS).
2. Nginx forwards the request to the appropriate backend server (e.g., Gunicorn running the Python app on `localhost:8000`).
3. The backend server processes the request and sends the response back to Nginx.
4. Nginx forwards the response to the client.

Here’s a sample Nginx configuration snippet to set it up as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;  # Forward requests to the backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
In this setup, Nginx acts as a reverse proxy that:

- Accepts HTTP requests from clients.
- Forwards them to a Python application server (e.g., Gunicorn running the Flask app).
- Receives the response and returns it to the client.
</details>
<details>
<summary>Use Nginx with Flask versus using Flask alone as a server</summary>

### 1. Flask as a Standalone Server
Flask includes a built-in development server (`flask run`) that you can use to serve your application. However, there are limitations:

- **Purpose:** Flask's built-in server is primarily for development and debugging, not for production.
- **Performance:** Flask's built-in server is single-threaded by default and does not handle high traffic well. It’s not designed for high concurrency or handling many simultaneous requests.
- **Features:** It lacks advanced server capabilities like load balancing, caching, SSL termination, or serving static content efficiently.

#### Example: Running Flask Alone
To run a Flask application standalone, you can use:

```bash
export FLASK_APP=app.py
flask run
```
Or, programmatically in `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask alone!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
#### Why Flask Alone May Be Insufficient
Flask’s built-in server is limited in:
- **Scalability:** It can’t handle high volumes of traffic or concurrent connections well.
- **Security:** It doesn’t handle HTTPS/SSL out of the box.
- **Reliability:** It’s not optimized for production environments and may crash under load or unexpected conditions.

### 2. Using Nginx with Flask (in Production)
To run Flask applications in a robust production environment, it’s common to use Nginx as a reverse proxy in front of a production-grade server like Gunicorn (a WSGI server that can run Flask). Here’s how it works:

Nginx receives incoming requests.
1. If the request is for static files, Nginx serves them directly, reducing load on the Flask app.
2. For other requests, Nginx forwards them to Gunicorn, which runs the Flask application.
3. Gunicorn processes the request and sends the response back to Nginx.
4. Nginx sends the final response to the client.

#### Example: Running Flask with Nginx and Gunicorn
1. Install Nginx and Gunicorn:
```bash
sudo apt install nginx
pip install gunicorn
```
2. Configure and run Gunicorn to serve the Flask app:

```bash
gunicorn --bind 127.0.0.1:8000 app:app
```
3. Configure Nginx as a reverse proxy for Gunicorn:

- Create a new Nginx configuration file (`/etc/nginx/sites-available/my_flask_app`):

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/files;
    }
}
```
- Link this file to Nginx’s `sites-enabled` and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/my_flask_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
### Summary: Flask Alone vs. Nginx with Flask

| Feature               | Flask Alone                     | Nginx with Flask and Gunicorn                 |
|-----------------------|---------------------------------|-----------------------------------------------|
| **Ease of Setup**     | Simple, quick setup            | More setup steps but manageable               |
| **Concurrency**       | Limited, single-threaded       | High, manages many simultaneous connections   |
| **Static File Handling** | Processed through Flask     | Handled by Nginx directly                     |
| **SSL/HTTPS**         | No built-in support            | SSL termination with Nginx                    |
| **Load Balancing**    | Not available                  | Load balancing across instances               |
| **Error Handling**    | Basic                          | Custom error pages, queueing, retry logic     |

#### Choosing Between Flask Alone and Nginx with Flask
- **Development:** Use Flask alone for simplicity.
- **Production:** Use Nginx with Gunicorn to handle higher traffic, enable SSL, and provide better security, reliability, and performance.
</details>
<details>
<summary>Workflow</summary>

### Workflow Overview
1. **Client Request:** A client (such as a browser or mobile app) sends an HTTP request to the server.
2. **Nginx:** Nginx receives the request first as the reverse proxy.
- Nginx can handle static files (like images, CSS, JavaScript) directly.
- For dynamic content, Nginx forwards the request to the WSGI server (e.g., Gunicorn).
3. **WSGI Server (Gunicorn):** The WSGI server receives the request from Nginx and passes it to the Python web application using the WSGI protocol.
4. **Application (Flask/Django):** The application processes the request, performs necessary operations (like querying a database), and generates a response.
5. **Response Flow Back:**
- The application sends the response back to the WSGI server.
- The WSGI server returns the response to Nginx.
- Nginx forwards the final response to the client.

### Detailed Workflow
1. **Client Requests:** A user on a browser or app requests a URL, say `https://example.com/home`.
```plaintext
GET /home HTTP/1.1
Host: example.com
```
2. **Nginx Handles the Request:**
- **Static Content:** If the request is for a static file (like `https://example.com/images/logo.png`), Nginx serves the file directly from disk.
    ```nginx
    location /images/ {
        alias /path/to/static/files/images/;
    }
    ```
    Nginx fetches logo.png from /path/to/static/files/images/ and sends it back to the client.

- **Dynamic Content:** If the request is for dynamic content (e.g., `/home`), Nginx forwards it to the WSGI server (Gunicorn) via a reverse proxy setup.
    ```nginx
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    ```
    The request is forwarded to Gunicorn listening on `localhost:8000`
3. **Nginx to Gunicorn:**
- Nginx acts as a reverse proxy and forwards dynamic requests to the Gunicorn server, configured to listen on a specific port (e.g., `localhost:8000`).
    ```plaintext
    GET /home HTTP/1.1
    Host: example.com
    X-Real-IP: 192.168.1.1
    X-Forwarded-For: 192.168.1.1
    ```
    Nginx includes headers like:
    + `X-Real-IP` for the client’s IP address.
    + `X-Forwarded-For` for tracking forwarded requests.
- Nginx communicates with Gunicorn via the HTTP protocol or Unix sockets.
4. **Gunicorn Receives the Request:**
- Gunicorn, as a WSGI server, receives the HTTP request from Nginx.
    + Command to Start Gunicorn:
    ```bash
    gunicorn --workers 4 --bind 127.0.0.1:8000 app:app
    ```
    + `app` is the Flask application file name.
    + `app` (second `app`) is the Flask application instance.
- Gunicorn then translates the HTTP request into a WSGI-compliant format and passes it to the Python application (e.g., Flask or Django).
5. **Flask/Django Application Processes the Request:**
The Flask application receives the WSGI-compliant request and processes it.
- The application processes the request, performs any necessary actions (e.g., reading from or writing to a database, running business logic), and creates an HTTP response (with status, headers, and body content).
lask Route:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/home')
def home():
    # Simulate some logic (e.g., database call)
    data = {"message": "Welcome to the Home Page!"}
    return jsonify(data)
```
6. **Response Back to Gunicorn:**
- The Flask or Django app sends the response back to Gunicorn.
Response Example:
    ```plaintext
    Status: 200 OK
    Headers: Content-Type: application/json
    Body: {"message": "Welcome to the Home Page!"}
    ```
- Gunicorn, as the WSGI server, wraps up the response and hands it back to Nginx.
7. **Nginx Returns the Response to the Client:**
- Nginx receives the response from Gunicorn.
- Nginx forwards the response back to the client’s browser or app.

#### Example Configuration (Nginx and Gunicorn)
- **Gunicorn Command:** Start the Gunicorn server to listen on port 8000:
```bash
gunicorn --workers 4 --bind 127.0.0.1:8000 myapp:app
```
- **Nginx Configuration:** Example Nginx configuration to pass requests to Gunicorn:
```nginx
server {
    listen 80;
    server_name example.com;

    location /static/ {
        alias /path/to/static/files;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
In this setup:
Static files are served by Nginx directly.
Dynamic requests (like /home) are forwarded to Gunicorn.
This combination creates a high-performance and scalable setup for serving Python web applications.
</details>
<details>
<summary>LAMP, SPOF, QPS</summary>

- **LAMP:** A common open-source web development stack. It stands for:

    + Linux: The operating system.
    + Apache: The web server.
    + MySQL: The database management system.
    + PHP (or sometimes Python or Perl): The programming language.

This stack is widely used for developing dynamic websites and applications.

- **SPOF (Single Point of Failure):** In a system or architecture, an SPOF is any individual component whose failure would cause the entire system to stop working. Reducing SPOFs is critical for high availability and reliability. Techniques to mitigate SPOFs include redundancy, load balancing, and failover systems.

- **QPS (Queries Per Second):** A measure of the number of queries a system can handle per second. It’s used to evaluate the performance and scalability of databases, search engines, and other systems that handle a large number of requests.
</details>


## Tasks
### 0. Simple web stack
A lot of websites are powered by simple web infrastructure, a lot of time it is composed of a single server with a [LAMP stack](https://en.wikipedia.org/wiki/LAMP_%28software_bundle%29).

On a whiteboard, design a one server web infrastructure that hosts the website that is reachable via `www.foobar.com`. Start your explanation by having a user wanting to access your website.

Requirements:
- You must use:
    + 1 server
    + 1 web server (Nginx)
    + 1 application server
    + 1 application files (your code base)
    + 1 database (MySQL)
    + 1 domain name `foobar.com` configured with a `www` record that points to your server IP `8.8.8.8`
- You must be able to explain some specifics about this infrastructure:
    + What is a server
    + What is the role of the domain name
    + What type of DNS record `www` is in `www.foobar.com`
    + What is the role of the web server
    + What is the role of the application server
    + What is the role of the database
    + What is the server using to communicate with the computer of the user requesting the website
- You must be able to explain what the issues are with this infrastructure:
    + SPOF
    + Downtime when maintenance needed (like deploying new code web server needs to be restarted)
    + Cannot scale if too much incoming traffic

### 1. Distributed web infrastructure
On a whiteboard, design a three server web infrastructure that hosts the website `www.foobar.com`.

Requirements:
- You must add:
    + 2 servers
    + 1 web server (Nginx)
    + 1 application server
    + 1 load-balancer (HAproxy)
    + 1 set of application files (your code base)
    + 1 database (MySQL)
- You must be able to explain some specifics about this infrastructure:
    + For every additional element, why you are adding it
    + What distribution algorithm your load balancer is configured with and how it works
    + Is your load-balancer enabling an Active-Active or Active-Passive setup, explain the difference between both
    + How a database Primary-Replica (Master-Slave) cluster works
    + What is the difference between the Primary node and the Replica node in regard to the application
- You must be able to explain what the issues are with this infrastructure:
    + Where are SPOF
    + Security issues (no firewall, no HTTPS)
    + No monitoring

### 2. Secured and monitored web infrastructure
On a whiteboard, design a three server web infrastructure that hosts the website `www.foobar.com`, it must be secured, serve encrypted traffic, and be monitored.

Requirements:
- You must add:
    + 3 firewalls
    + 1 SSL certificate to serve `www.foobar.com` over HTTPS
    + 3 monitoring clients (data collector for Sumologic or other monitoring services)
- You must be able to explain some specifics about this infrastructure:
    + For every additional element, why you are adding it
    + What are firewalls for
    + Why is the traffic served over HTTPS
    + What monitoring is used for
    + How the monitoring tool is collecting data
    + Explain what to do if you want to monitor your web server QPS
- You must be able to explain what the issues are with this infrastructure:
    + Why terminating SSL at the load balancer level is an issue
    + Why having only one MySQL server capable of accepting writes is an issue
    + Why having servers with all the same components (database, web server and application server) might be a problem

3. Scale up
Readme
- [Application server vs web server](https://www.f5.com/glossary)

Requirements:
- You must add:
    + 1 server
    + 1 load-balancer (HAproxy) configured as cluster with the other one
    + Split components (web server, application server, database) with their own server
- You must be able to explain some specifics about this infrastructure:
    + For every additional element, why you are adding it
