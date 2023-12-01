# Application Server vs Web Server

## Application Server
An application server is a specialized server responsible for executing the code that makes up an application. It handles the processing of dynamic content, interacts with databases, and manages various application-related tasks. Its primary role is to execute and deliver application-specific functionalities to users or clients.

### Why an Application Server?
An application server is added to handle the execution of application-specific code separately from serving web content. It ensures efficient processing and management of dynamic functionalities, such as user authentication, data processing, and business logic implementation.

## Web Server
A web server's primary function is to serve static content, handle HTTP requests, and deliver web pages to users or clients. It manages incoming requests, processes them, and serves static resources like HTML, CSS, and images.

### Why a Web Server?
A web server is included to efficiently handle and serve static content, optimizing the delivery of web pages and resources to users. It works alongside the application server to serve the required web content.

---

## Infrastructure Details

### Components Added:
- **One Server**: Hosting components individually, including the web server, application server, and database.
- **Load-Balancer (HAproxy) Cluster Configuration**: Configured as a cluster to enhance load distribution and provide high availability.

### Role of Additional Elements:
- **Load-Balancer Cluster**: Used to evenly distribute incoming traffic across multiple instances of web servers or application servers, improving performance and availability.
- **Split Components**: Separate servers for web, application, and database components provide isolation, scalability, and better resource management.

### Explanation:
The addition of separate servers for distinct components (web, application, database) allows for a more organized and scalable infrastructure setup. The load balancer configured as a cluster ensures efficient traffic distribution and reliability, while distinct servers for each component enable better resource utilization and scalability.

This setup ensures that the web server serves static content, the application server manages application-specific logic, and the database server handles data storage and retrieval.

