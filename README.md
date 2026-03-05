# Chat-Application-with-Socket-Programming
This project is a simple chat application, similar to WhatsApp or Messenger, designed to explore socket programming. The application allows users to send messages and files to each other.

The server is multi-threaded and capable of handling multiple client connections concurrently.


**Client Features**

Send Messages: Users can send messages to other connected clients by specifying their usernames.

List Available Users: Users can view a list of all connected clients, including themselves.

File Transfer: Users can send files to other connected clients. The recipients save the file with their username prefixed to the original filename.

Help Command: Users can view a list of all supported commands and their syntax.

Quit Command: Users can disconnect from the server gracefully.

**Server Features**

Multi-threaded: The server can handle multiple clients concurrently, up to a specified maximum number (MAX_NUM_CLIENTS).

Client Management: The server manages client connections, ensuring unique usernames and handling client disconnections gracefully.

Message and File Forwarding: The server forwards messages and files to the intended recipients.

Error Handling: The server handles various error conditions, such as server full or username already taken.
