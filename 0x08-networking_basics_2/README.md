# 0x08. Networking basics #1
## Resources
- [What is localhost](https://en.wikipedia.org/wiki/Localhost)
- [What is 0.0.0.0](https://en.wikipedia.org/wiki/0.0.0.0)
- [What is the hosts file](https://www.makeuseof.com/tag/modify-manage-hosts-file-linux/)
- [Netcat examples](https://www.thegeekstuff.com/2012/04/nc-command-examples/)

**man or help:**
- `ifconfig`
- `telnet`
- `nc`
- `cut`

## Learning Objectives
<details>
<summary>What is localhost/127.0.0.1</summary>

### localhost/127.0.0.1
Localhost is a hostname that refers to the device you are currently using. It represents the local computer in networking, allowing you to communicate within the device itself without needing an external network connection.
- **IP Address:** Localhost is mapped to the IP address **127.0.0.1** (for IPv4) and ::1 (for IPv6).
- **Purpose:** Often used for testing and development purposes, localhost allows applications or services to interact with each other on the same machine. For example, when setting up a local web server, accessing 127.0.0.1 in a browser will connect to the server running on your device.

#### Key Points about Localhost / `127.0.0.1`:
- **Loopback Interface:** The loopback interface is a virtual network interface on a computer that routes traffic back to itself.
- **No External Connection:** Connections to localhost don’t leave the device, making it useful for secure and isolated testing.
- **Common Use Cases:** Developers use localhost to test web applications, databases, or network configurations locally before deploying them to a live server.
</details>
<details>
<summary>What is 0.0.0.0</summary>

### What is 0.0.0.0
The IP address 0.0.0.0 has a special meaning in networking:

#### 1. Wildcard Address: 
To make a server listen on all network interfaces, you can specify `0.0.0.0` as the binding address in your server’s configuration. This allows the server to accept connections from any IP address assigned to your device.

When you make a server listen on all network interfaces by binding it to `0.0.0.0`, you’re telling the server to accept connections coming from any network that the device is connected to. This includes connections from:

- **Local Network Interfaces:** Like the loopback interface (`127.0.0.1`), which is accessible only from the same device.
- **Public and Private IP Addresses:**Such as a local IP (`192.168.x.x` or `10.x.x.x`) for internal network access, or a public IP if the device is directly accessible from the internet.

**Example Scenario**
Imagine you have a computer running a web server, and this computer has two network interfaces:
- Wi-Fi network with an IP like `192.168.1.10`
- Ethernet network with an IP like `192.168.2.20`

By binding the server to `0.0.0.0`, you enable it to accept requests on both interfaces:
- A user on the Wi-Fi network could connect to `192.168.1.10`
- A user on the Ethernet network could connect to `192.168.2.20`

In contrast, if you bind the server to a specific IP (e.g., `127.0.0.1`), only requests to that IP would be accepted, limiting access to connections from the same device.

**Example Usage:**
- **Web Server (Python’s Flask):**

    ```python
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Hello, World!"

    if __name__ == "__main__":
        # Bind to all interfaces
        app.run(host="0.0.0.0", port=5000)
    ```
    Here, host="0.0.0.0" allows the Flask app to accept connections from any network interface on port 5000.

- **Node.js Server:**
    ```javascript
    const http = require("http");

    const server = http.createServer((req, res) => {
    res.end("Hello, World!");
    });

    // Bind to all interfaces
    server.listen(3000, "0.0.0.0", () => {
    console.log("Server listening on port 3000");
    });
    ```
Setting `0.0.0.0` here allows the server to listen on all interfaces, accepting incoming connections from any IP address on port 3000.
#### 2. Unspecified Address:
**DHCP (Dynamic Host Configuration Protocol)** is a network management protocol used to automatically assign IP addresses and other network configuration settings to devices on a network. This process eliminates the need for manual configuration of each device, making it easier to connect multiple devices to a network without administrative overhead.

When a device is in the process of obtaining an IP address, it may temporarily use `0.0.0.0` as a placeholder, especially in DHCP configuration. Generally, you don’t manually configure `0.0.0.0` for this purpose; instead, this is managed automatically by the DHCP client during the IP acquisition process.

**Example Usage:**
DHCP Lease Request: Devices might show `0.0.0.0` in DHCP logs or status screens before they have been assigned a specific IP address by the DHCP server. You would typically see this address on interfaces before they’re configured with a valid IP.

#### 3. Routing Placeholder:
In routing tables, `0.0.0.0` can represent the default route (or “gateway of last resort”), directing traffic to an external network, typically the internet, when no other routes match.
Example Usage: Linux Routing Table:
```bash
sudo ip route add default via 192.168.1.1
```
This command uses default, which is equivalent to `0.0.0.0/0`, to route all non-specific traffic to `192.168.1.1`, the gateway IP.
</details>
<details>
<summary>What is /etc/hosts</summary>

### /etc/hosts file
It is a simple text file used by operating systems to map hostnames to IP addresses. It's a local DNS (Domain Name System) resolution mechanism that allows a system to associate a human-readable domain name (like `example.com`) with an IP address (like `192.168.1.1`) without needing to query an external DNS server.

#### Structure of `/etc/hosts`
The file contains lines of text, with each line mapping an IP address to one or more hostnames. The general syntax is:
```css
IP_address    hostname    [aliases...]
```

#### Example:
```lua
127.0.0.1   localhost
192.168.1.1 router
192.168.1.10 webserver.local webserver
```
In this example:
- `127.0.0.1` is associated with `localhost`, the loopback address used for local communication within the same machine.
- `192.168.1.1` is mapped to `router`, typically the local gateway IP.
- `192.168.1.10` is mapped to both `webserver.local` and `webserver`, so either name can be used to refer to that IP.

#### Functions of `/etc/hosts`:
1. **Local Name Resolution:** It allows the system to resolve hostnames to IP addresses locally, without relying on an external DNS server.
2. **Override DNS:** Entries in `/etc/hosts` can override DNS lookups for specific domain names, providing a way to force specific resolutions (useful for local development or testing).
3. **Network Troubleshooting:** It can be useful for network diagnostics or configuration, ensuring certain addresses always resolve in a specific way.

#### Common Usage:
- **Local Development:** Developers often use `/etc/hosts` to map a custom domain name (like `dev.local`) to `127.0.0.1` or a local IP for testing purposes.
- **Blocking Sites:** Some users place entries in `/etc/hosts` to block websites by mapping them to `127.0.0.1` (e.g., `0.0.0.0 example.com`).
- **Network Configuration:** In local networks, `/etc/hosts` can map machine names to IP addresses for easy access without needing a DNS server.

#### Important Considerations:
- **Order Matters:** The system will process entries from top to bottom, so the first matching entry is used for a hostname lookup.
- **Permissions:** Only users with root privileges (or sudo access) can modify the `/etc/hosts` file, as it is a system-wide configuration file.
</details>
<details>
<summary>How to display your machine’s active network interfaces</summary>

### Display machine's active network interfaces

1. **`ip` command**
    ```bash
    ip a
    ```
    - This will display detailed information about all network interfaces, including their IP addresses, MAC addresses, and other settings.
    - Active interfaces will be shown with an IP address and status (e.g., `UP`).
2. **`ifconfig` command** (older systems)
    ```bash
    ifconfig
    ```
    This command is used on older Linux distributions or systems where ifconfig is still available. It will show the status and configuration of all network interfaces.
3. **`nmcli` (NetworkManager)** for systems using NetworkManager
    ```bash
    nmcli device status
    ```
    This command lists all network devices and their status (whether they are connected or disconnected).
4. **`netstat`**
    The `netstat` command can be used to display active network connections, which can give you a clue about which network interfaces are in use:
    ```bash
    netstat -i
    ```
    This shows a summary of network interfaces with data on packets transmitted and received.

</details>
<details>
<summary>What's a Network Interface</summary>

### Network Interface
A network interface refers to a point of connection through which a device communicates over a network. It acts as the interface between the device (like a computer, server, or router) and the network, enabling it to send and receive data. In simpler terms, it is the hardware or virtual device that connects your computer to a network.

#### Types of Network Interfaces:
##### 1. Physical Network Interfaces:
- **Ethernet Interface** (wired connection): A physical port on your device where you connect an Ethernet cable to a router or switch. It usually corresponds to a device like `eth0` or `enp3s0` on Linux, `en0` or `en1` on macOS.
- **Wi-Fi Interface** (wireless connection): A wireless adapter on your device that connects to a Wi-Fi network. It might be named something like `wlan0` on Linux or `en1` on macOS.

##### 2. Virtual Network Interfaces:
- **Loopback Interface:** A virtual interface that allows a device to communicate with itself. It typically uses the IP address `127.0.0.1` and is represented by `lo` in Linux and macOS. It is useful for testing and troubleshooting.
- **VPN Interface:** A virtual interface created when you connect to a Virtual Private Network (VPN), allowing secure communication over the internet or a remote network.
- **Bridged Interfaces:** Virtual interfaces created to connect virtual machines or containers to the network, typically used in virtualization environments.

##### 3. Specialized Network Interfaces:
- **Bluetooth Interface:** For short-range wireless communication between devices like a smartphone and computer.
- **Mobile Data Interface:** For connecting to mobile networks via a device’s cellular modem, typically found on smartphones or dedicated mobile hotspots.

#### Key Aspects:
- **IP Address:** Each network interface on a device can have its own IP address. For example, a laptop might have one IP address for its Ethernet interface and another for its Wi-Fi interface.
- **MAC Address:** A unique identifier assigned to each physical network interface, used at the data link layer for local network communication.
- **Interface Status:** A network interface can be **active** (up and running) or **inactive** (down), depending on whether it’s connected to a network.

#### Example:
A computer connected to both a wired Ethernet network and a wireless Wi-Fi network will have **two network interfaces**: one for Ethernet (`eth0` or `enp3s0`) and one for Wi-Fi (`wlan0` or `en1`).
Each of these interfaces has its own configuration (e.g., IP address, subnet mask) and can be used independently or simultaneously depending on the system's network settings.
</details>
<details>
<summary>What is Telnet</summary>

### Telnet
Telnet (short for "Telecommunication Network") is a network protocol used to provide a command-line interface for communication with remote devices over a TCP/IP network. It allows a user to log into a remote machine and execute commands on it, making it one of the earliest remote access protocols.

However, Telnet sends data, including login credentials, in plaintext, which makes it insecure for modern use in most environments. Because of this, it has largely been replaced by more secure protocols like SSH (Secure Shell).

#### Key Features of Telnet:
- **Remote Access:** Allows users to remotely log into systems and manage them.
- **Command-Line Interface:** Provides a terminal-like interface to execute commands on a remote machine.
- **Insecure:** Telnet does not encrypt the data, so it is vulnerable to interception and man-in-the-middle attacks.

#### How to Use Telnet
**1. Installing Telnet** (if not installed)
```bash
sudo apt-get install telnet
```
**2. Using Telnet**
Basic Telnet Command Syntax:
```bash
telnet [hostname or IP address] [port number]
```
- hostname or IP address: The remote server’s domain name or IP address.
- port number: The port you want to connect to (optional, default is 23).

Example: Connecting to a remote server:
```bash
telnet example.com 23
```
Or, if the server only uses Telnet on a different port:
```bash
telnet example.com 80  # Connect to port 80 (HTTP)
```
Once connected, you will be able to interact with the remote machine (if Telnet service is running on the target).

**Basic Commands After Connecting:**
- **Login:** If the Telnet server requires authentication, you will be prompted to log in with a username and password.
- **Exit:** To disconnect from the session, you can type `exit` or press **Ctrl+]** (this takes you to the Telnet prompt, then type `quit`).

**Telnet Prompt:**
If you're at the Telnet prompt (after pressing **Ctrl+]**), you can use commands like:
- **quit:** Close the connection.
- **status:** Show the current status of the connection.
- **open:** Open a new connection to another host.

Example of Using Telnet to Connect:
```bash
$ telnet example.com
Trying 93.184.216.34...
Connected to example.com.
Escape character is '^]'.

Welcome to example.com!
login: user
Password: ********
$ exit
Connection closed.
```
#### Common Uses of Telnet:
1. **Testing Connections:** Telnet can be used to test if a port on a remote server is open and accessible. For example:

Check if HTTP (port 80) is open on a server:
```bash
telnet example.com 80
```
If the connection succeeds, you can then send HTTP commands to the server.
2. **Troubleshooting Network Issues:** You can use Telnet to check the availability of services running on a specific port. If Telnet cannot connect, the port may be closed, or there may be a firewall issue.

3. **Remote Administration:** Historically, Telnet was used to access remote devices (like routers or switches) and manage them through a command-line interface. However, due to its lack of encryption, SSH has replaced Telnet for secure remote administration.

#### Limitations:
- **Security:** Telnet transmits data in plaintext, including usernames and passwords. This makes it vulnerable to eavesdropping and attacks.
- **No Encryption:** Data sent via Telnet is not encrypted, so it's unsuitable for sensitive information or modern network management.
</details>
<details>
<summary>What is nc and how to use it</summary>

### nc (Netcat)
Netcat (nc) is a versatile networking tool used for reading from and writing to network connections using the **TCP** or **UDP** protocols. Often referred to as the "Swiss army knife" of networking, Netcat is commonly used for tasks like:
- Establishing network connections
- Testing network services
- Debugging or monitoring network traffic
- Port scanning
- Creating simple network servers or clients

It is known for being lightweight, easy to use, and highly powerful in both interactive and scripting contexts.

#### Features of Netcat:
- Can create TCP and UDP connections to remote systems.
- Can be used as a client or server in a network communication.
- Can transfer data to/from a network connection (useful for troubleshooting or file transfers).
- Can be used to scan ports on a system.
- Supports both IPv4 and IPv6.

**Basic Syntax:**
    ```bash
    nc [options] [hostname] [port]
    ```

#### How to Use nc (Netcat)
##### 1. Creating a Simple TCP Server (Listening Mode)
To start a server that listens on a specific port:
```bash
nc -l -p 1234
```
- **-l**: Tells Netcat to listen for incoming connections. Essentially turning the machine into a server. Without this, Netcat would try to connect to a remote machine (as a client) instead.
- **-p 1234**: Specifiesthat the server should listen on port `1234`. 

Netcat starts a server on your local machine, listening for incoming TCP connections on port `1234`.
**How Does This Work?**
1. The server (your machine) is waiting for connections on port `1234`.
2. A client (another machine) can then connect to this server by using the IP address of your machine and the port number 1234.
For example, if the client machine knows your laptop's IP address is 192.168.1.10, it can try to connect to the server (your laptop) like this:
```bash
nc 192.168.1.10 1234
```
Once the connection is made:
- Anything typed on the client machine will appear on the server machine.
- Similarly, anything typed on the server machine will appear on the client.

**Example Use Cases:**
1. Testing a Client-Server Connection:
- Run `nc -l -p 1234` on your server.
- On the client side, use `nc [server-ip] 1234` to connect to the server and start sending data back and forth.
2. Creating a Simple Chat Server:
- Server side: `nc -l -p 1234`
- Client side: `nc [server-ip] 1234`
- You can now send messages between the server and client.
3. Checking a Firewall or Port Configuration:
- If you're unsure if a specific port is open and accessible, you can use `nc -l -p [port]` to ensure that your machine is listening on that port and then check it from a remote machine using `nc [server-ip] [port]`.
4. Proxying Data (Using nc in Listening Mode with Data Forwarding)
- Netcat is commonly used to forward network traffic. For example, you can use `nc` in listening mode to act as a proxy between two devices by forwarding incoming data to a different destination:
```bash
nc -l -p 1234 | nc [destination-ip] [destination-port]
```
This command listens on port `1234` and forwards the traffic to another server.
**Summary**
When you run `nc -l -p 1234`, you are creating a **TCP server** on the machine where you run this command. This server listens for incoming connections on port `1234`. Another machine (client) can connect to this server using your machine’s IP address and port `1234`, allowing both machines to send and receive data.
##### 2. Connecting to a Remote Server
To connect to a remote server (as a client):
```bash
nc example.com 80
```
This connects to `example.com` on port `80` (HTTP). Once connected, you can send data (like HTTP requests) directly from the terminal.

##### 3. Sending Data to a Remote Server
You can send data to a server by typing after connecting:
```bash
nc example.com 80
GET / HTTP/1.1
Host: example.com
```
Press Enter twice to send the request. The web server will respond with an HTTP response.

##### 4. File Transfer Using Netcat (Client-Server)
Netcat can also be used to transfer files between systems.

- **On the receiving machine (Server):**
    ```bash
    nc -l -p 1234 > received_file.txt
    ```
This tells Netcat to listen on port `1234` and save the incoming data to `received_file.txt`.

- **On the sending machine (Client):**
    ```bash
    nc target_ip 1234 < file_to_send.txt
    ```
This connects to the receiving machine’s IP on port `1234` and sends the contents of `file_to_send.txt`.

##### 5. Port Scanning
Netcat can be used as a simple port scanner to check which ports are open on a remote system.

```bash
nc -zv example.com 20-80
```
- **-z**: Scans without sending any data (just checks if the port is open).
- **-v**: Makes the output verbose, showing which ports are open.

This command scans ports `20` to `80` on `example.com` and displays whether each port is open.
##### 6. UDP Mode
Netcat can also work with the UDP protocol. To set up a UDP listener:
```bash
nc -l -u -p 1234
```
- **-u**: Tells Netcat to use UDP instead of TCP.
- **-p 1234**: Specifies the UDP port (1234).

To send a message to this listener from another machine:
```bash
nc -u target_ip 1234
```
##### 7. Creating a Simple Chat Server
You can use Netcat to create a simple chat server, where multiple clients can send messages to each other.

**On the server:**
```bash
nc -l -p 1234
```
**On the client (another terminal):**
```bash
nc server_ip 1234
```
Now, anything typed on the client terminal will appear on the server’s terminal, and vice versa.

#### Common Netcat Options:
- **-l**: Listen for incoming connections (server mode).
- **-p**: Specify the port number.
- **-z**: Scan for open ports without sending any data.
- **-v**: Verbose output; useful for seeing more details.
- **-u**: Use UDP instead of the default TCP.
- **-w [seconds]**: Set a timeout (in seconds) for connections.
- **-e [program]**: Executes a program after the connection is established (useful for creating reverse shells).

</details>
<details>
<summary>What is cut and how to use it</summary>

### `cut` command
The `cut` command in Unix/Linux is used to remove sections from each line of a file or from the output of a command. It allows you to extract specific columns or fields from text files or command output, typically delimited by characters such as spaces, tabs, or commas.

**Basic Syntax:** `cut OPTION [FILE]`
Where `OPTION` defines how the text is cut, and `[FILE]` is the input file. If no file is provided, it processes standard input (stdin).

**Common Options for `cut`:**
- `-b` : Select specific bytes from each line.
- `-c` : Select specific characters from each line.
- `-f` : Select specific fields (columns) from each line (useful for delimited files).
- `-d` : Define a custom delimiter (default is tab).
- `-s` : Suppress lines that do not contain the delimiter.
- `--complemen`t : Invert the selection (select everything except the specified fields).

#### Examples:
1. **Extract specific fields (columns) from a CSV file:** Let's say you have a CSV file (data.csv) with the following content:
    ```
    Name,Age,Occupation
    Alice,30,Engineer
    Bob,25,Artist
    Charlie,35,Doctor
    ```
    To extract the `Name` and `Occupation` columns:

    ```bash
    cut -d ',' -f 1,3 data.csv
    ```
    - `-d ','` specifies the delimiter (comma).
    - `-f 1,3` specifies the fields to extract (field 1 is `Name`, field 3 is `Occupation`).

    Output:
    ```
    Name,Occupation
    Alice,Engineer
    Bob,Artist
    Charlie,Doctor
    ```
2. **Extract characters by position:** Suppose you have a file ``example.txt`` with the following content:
    ```
    hello
    world
    example
    ```
    To extract the first 3 characters from each line:
    ```bash
    cut -c 1-3 example.txt
    ```
    Output:
    ```
    hel
    wor
    exa
    ```
3. **Extract a specific byte range:** If you want to select the first 5 bytes of each line:
    ```bash
    cut -b 1-5 example.txt
    ```
    Output:
    ```
    hello
    world
    examp
    ```
4. **Extract specific fields, ignoring lines without the delimiter:** If your data contains missing or malformed entries:
```bash
cut -d ',' -f 1 -s data.csv
```
The `-s` option ensures that lines without a delimiter are skipped.

5. **Use `cut` in a pipeline:** You can use `cut` to process the output of other commands. For example, using `ps` to list processes and extracting the process ID and the command name:

```bash
ps aux | cut -d ' ' -f 1,11
```
</details>
<details>
<summary>What is ifconfig and how to use it</summary>

### `ifconfig` command
`ifconfig` (interface configuration) is a command-line tool used to configure, manage, and display network interfaces on a Linux or Unix-based system. It provides detailed information about the system's network interfaces, such as their IP addresses, MAC addresses, status, and other network-related configurations.

Note: On newer Linux distributions, `ifconfig` is being replaced by `ip`, but `ifconfig` is still widely used and available on many systems.

**Basic Syntax:** `ifconfig [interface] [options]`
- If no interface is specified, `ifconfig` will display information about all active network interfaces.
- If an interface name (like eth0, wlan0) is provided, `ifconfig` will only show or configure that interface.

#### Common Uses of `ifconfig`:
##### 1. Display Network Interfaces Information
To display information about all active network interfaces:
```bash
ifconfig
```
This command shows details about each interface, including:
- Interface name (e.g., `eth0`, `lo`, `wlan0`).
- IP address (both IPv4 and IPv6).
- MAC address (physical address).
- MTU (Maximum Transmission Unit).
- RX/TX packets (packets received/transmitted).
- Errors (RX-ERR, TX-ERR, RX-DRP, TX-DRP).
- Flags (interface status such as up, broadcast, etc.).

##### 2. Display Information for a Specific Interface
To show details for a specific network interface, specify its name:
```bash
ifconfig eth0
```
This will show information only for the `eth0` interface.

##### 3. Assign an IP Address to an Interface
You can assign a static IP address to a network interface using ifconfig. For example, to assign IP `192.168.1.10` to the `eth0` interface:
```bash
sudo ifconfig eth0 192.168.1.10
```
To set the subnet mask to 255.255.255.0:
```bash
sudo ifconfig eth0 192.168.1.10 netmask 255.255.255.0
```
##### 4. Activate or Deactivate an Interface
To bring up (activate) a network interface:
```bash
sudo ifconfig eth0 up
```
To bring down (deactivate) the interface:

```bash
sudo ifconfig eth0 down
```
##### 5. View or Change the MAC Address
To view the MAC address of an interface:
```bash
ifconfig eth0
```
The MAC address will be listed under the `HWaddr` section.

To change the MAC address of a network interface:
```bash
sudo ifconfig eth0 hw ether 00:11:22:33:44:55
```
##### 6. Set the Interface to Obtain an IP Address via DHCP
To configure an interface to automatically obtain an IP address using DHCP:
```bash
sudo ifconfig eth0 up
sudo dhclient eth0
```
Alternatively, the `dhclient` command is often used separately to request an IP from a DHCP server.

##### 7. Set the Broadcast Address
To configure a specific broadcast address:
```bash
sudo ifconfig eth0 broadcast 192.168.1.255
```
##### 8. View or Set the MTU (Maximum Transmission Unit)
To view the MTU value of an interface:
```bash
ifconfig eth0
```
To set a new MTU value:
```bash
sudo ifconfig eth0 mtu 1500
```
##### 9. Check the Interface’s RX/TX Stats
`ifconfig` provides detailed statistics about received (RX) and transmitted (TX) packets for each interface, including:
- RX-OK: Received packets without error.
- RX-ERR: Packets received with errors.
- TX-OK: Transmitted packets without error.
- TX-ERR: Packets transmitted with errors.
- RX-DRP: Dropped received packets.
- TX-DRP: Dropped transmitted packets.
##### 10. Assign Multiple IPs to an Interface
You can assign multiple IP addresses to the same interface by specifying additional aliases. For example, to add IP `192.168.1.20` to `eth0`:
```bash
sudo ifconfig eth0:0 192.168.1.20
```
**Example Outputs of `ifconfig`:**
Output of `ifconfig` with no arguments:

```arduino
eth0      Link encap:Ethernet  HWaddr 00:1a:2b:3c:4d:5e  
          inet addr:192.168.1.10  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::21a:2bff:fe3c:4d5e/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:3456 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2345 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:3456789 (3.4 MB)  TX bytes:2345678 (2.3 MB)
Output for the lo (loopback) interface:

sql
lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:789 errors:0 dropped:0 overruns:0 frame:0
          TX packets:789 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:456789 (456.7 KB)  TX bytes:456789 (456.7 KB)
```
</details>

## Tasks
### 0. Change your home IP
Write a Bash script that configures an Ubuntu server with the below requirements.
Requirements:
- `localhost` resolves to `127.0.0.2`
- `facebook.com`resolves to `8.8.8.8`.
- The checker is running on Docker, so make sure to read [this](http://blog.jonathanargentiero.com/docker-sed-cannot-rename-etcsedl8ysxl-device-or-resource-busy/)
```bash
sylvain@ubuntu$ ping localhost
PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.012 ms
^C
--- localhost ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.012/0.012/0.012/0.000 ms
sylvain@ubuntu$
sylvain@ubuntu$ ping facebook.com
PING facebook.com (157.240.11.35) 56(84) bytes of data.
64 bytes from edge-star-mini-shv-02-lax3.facebook.com (157.240.11.35): icmp_seq=1 ttl=63 time=15.4 ms
^C
--- facebook.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 15.432/15.432/15.432/0.000 ms
sylvain@ubuntu$
sylvain@ubuntu$ sudo ./0-change_your_home_IP
sylvain@ubuntu$
sylvain@ubuntu$ ping localhost
PING localhost (127.0.0.2) 56(84) bytes of data.
64 bytes from localhost (127.0.0.2): icmp_seq=1 ttl=64 time=0.012 ms
64 bytes from localhost (127.0.0.2): icmp_seq=2 ttl=64 time=0.036 ms
^C
--- localhost ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.012/0.024/0.036/0.012 ms
sylvain@ubuntu$
sylvain@ubuntu$ ping facebook.com
PING facebook.com (8.8.8.8) 56(84) bytes of data.
64 bytes from facebook.com (8.8.8.8): icmp_seq=1 ttl=63 time=8.06 ms
^C
--- facebook.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 8.065/8.065/8.065/0.000 ms
```
In this example we can see that:
- before running the script, `localhost` resolves to `127.0.0.1` and facebook.com resolves to `157.240.11.35`
- after running the script, `localhost` resolves to `127.0.0.2` and facebook.com resolves to `8.8.8.8`

If you’re running this script on a machine that you’ll continue to use, be sure to revert localhost to `127.0.0.1`. Otherwise, a lot of things will stop working!

### 1. Show attached IPs
Write a Bash script that displays all active IPv4 IPs on the machine it’s executed on.
```bash
sylvain@ubuntu$ ./1-show_attached_IPs | cat -e
10.0.2.15$
127.0.0.1$
```
Obviously, the IPs displayed may be different depending on which machine you are running the script on.

Note that we can see our `localhost` IP :)

### 2. Port listening on localhost
Write a Bash script that listens on port `98` on `localhost`.

**Terminal 0**

Starting my script.
```bash
sylvain@ubuntu$ sudo ./100-port_listening_on_localhost
```
**Terminal 1**
Connecting to `localhost` on port `98` using `telnet` and typing some text.
```bash
sylvain@ubuntu$ telnet localhost 98
Trying 127.0.0.2...
Connected to localhost.
Escape character is '^]'.
Hello world
test
```
**Terminal 0**
Receiving the text on the other side.
```bash
sylvain@ubuntu$ sudo ./100-port_listening_on_localhost
Hello world
test
```
For the sake of the exercise, this connection is made entirely within `localhost`. This isn’t really exciting as is, but we can use this script across networks as well. Try running it between your local PC and your remote server for fun!

As you can see, this can come in very handy in a multitude of situations. Maybe you’re debugging socket connection issues, or you’re trying to connect to a software and you are unsure if the issue is the software or the network, or you’re working on firewall rules… Another tool to add to your debugging toolbox!
