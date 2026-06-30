import streamlit as st

def main():
    st.header("System Calls")
    st.write("""
1. **socket()**: Creates an endpoint for communication and returns a file descriptor for the socket.
2. **setsockopt()**: Sets options on the socket, such as allowing multiple connections.
3. **bind()**: Binds the socket to a specific address and port.
4. **listen()**: Marks the socket as a passive socket that will be used to accept incoming connection requests.
5. **accept()**: Accepts an incoming connection on a listening socket.
6. **poll()**: Monitors multiple file descriptors to see if any have any pending events.
7. **read()**: Reads data from a file descriptor.
8. **send()**: Sends data to a connected socket.
9. **close()**: Closes a file descriptor, so that it no longer refers to any file and may be reused.
""")


    st.header("System Call Program")
    st.write("""
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <poll.h>

#define PORT 8080
#define MAX_CLIENTS 10

int main() {
    int master_socket, new_socket, client_sockets[MAX_CLIENTS];
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    int opt = 1;
    int activity, i, valread;
    char buffer[1024] = {0};
    struct pollfd fds[MAX_CLIENTS + 1];

    // Create a master socket
    if ((master_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Set master socket to allow multiple connections
    if (setsockopt(master_socket, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    // Bind the socket to localhost and port
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(master_socket, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Specify maximum of 3 pending connections for the master socket
    if (listen(master_socket, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    // Accept the incoming connection
    puts("Waiting for connections ...");

    // Initialize the client sockets array
    for (i = 0; i < MAX_CLIENTS; i++) {
        client_sockets[i] = 0;
    }

    // Add master socket to the set
    fds[0].fd = master_socket;
    fds[0].events = POLLIN;

    while (1) {
        // Use poll to wait for events on the sockets
        activity = poll(fds, MAX_CLIENTS + 1, -1);
        if (activity < 0) {
            perror("poll error");
            exit(EXIT_FAILURE);
        }

        // Handle incoming connections
        if (fds[0].revents & POLLIN) {
            if ((new_socket = accept(master_socket, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
                perror("accept");
                exit(EXIT_FAILURE);
            }

            // Inform user of socket number
            printf("New connection, socket fd is %d, IP is : %s, port : %d\\n", new_socket, inet_ntoa(address.sin_addr), ntohs(address.sin_port));

            // Add new socket to the client sockets array
            for (i = 0; i < MAX_CLIENTS; i++) {
                if (client_sockets[i] == 0) {
                    client_sockets[i] = new_socket;
                    break;
                }
            }

            // Add new socket to pollfds array
            fds[i+1].fd = new_socket;
            fds[i+1].events = POLLIN;
        }

        // Handle data from clients
        for (i = 1; i <= MAX_CLIENTS; i++) {
            if (fds[i].revents & POLLIN) {
                if ((valread = read(fds[i].fd, buffer, 1024)) == 0) {
                    // Client disconnected
                    close(fds[i].fd);
                    client_sockets[i - 1] = 0;
                    printf("Client disconnected: socket fd %d\\n", fds[i].fd);
                } else {
                    // Echo back the message
                    send(fds[i].fd, buffer, valread, 0);
                }
            }
        }
    }

    return 0;
}""")

    st.header("Output")
    st.image("output.png")
