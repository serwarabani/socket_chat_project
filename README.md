# Socket Chat Application

A multi-client, real-time chat application built with Python, utilizing socket programming, multi-threading, and Tkinter for a graphical user interface.

## 👥 Project Members
- **[Serve Rabani and Maryam Karimi]** - [GitHub Profile](https://github.com/serwarabani)

---

## 🛠 Project Implementation Details

### Phase 1: Basic Connection
The foundation of the project. A basic server-client architecture was established using TCP sockets to exchange simple text messages.
* **Implementation:** `socket` library was used to bind the server to a specific port and allow a client to connect.

### Phase 2: Multi-Client Support
The server was upgraded to support multiple simultaneous users.
* **Implementation:** The `threading` module was utilized to spawn a new thread for every incoming client, ensuring the server remains responsive.

### Phase 3: Broadcast & Secure Disconnection
Implementation of group messaging and session management.
* **Implementation:** A `broadcast` function distributes messages to all clients. The `/exit` command ensures the socket is closed gracefully.

### Phase 4: GUI & Advanced Features
Integration of a graphical user interface and advanced messaging protocols.
* **Implementation:** 
    * **GUI:** Built with `Tkinter`.
    * **Private Messaging:** Added `>pm <IP> <Message>` using a dictionary mapping.
    * **User Tracking:** Added `>users` command to list active participants.
    * **Timestamping:** Every message is timestamped using the `datetime` module.

---

## 📸 Screenshots

### 1. Main Chat Interface
![Chat GUI](phase4_gui.png)

### 2. User List (>users)
![User List](users_list.png)

### 3. Private Messaging (>pm)
![Private Message](pm_demo.png)

---

## 🚀 How to Run

1. **Start the Server:**
   ```bash
   python server.py