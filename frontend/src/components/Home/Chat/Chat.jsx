import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import axios from "axios";
import userDefaultPfp from "../../../assets/images/userDefaultPfp.png";
import "./Chat.css";

const Chat = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get("http://localhost:8006/users/all");
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      console.error("Access token is missing");
      return;
    }

    const socketInstance = io("http://localhost:8009", {
      path: "sockets", 
      extraHeaders: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    

    socketInstance.on("connect", () => {
      console.log("Connected to Socket.IO!");
    });

    socketInstance.on("receive_message", (message) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { from_user_id: message.from_user_id, content: message.content },
      ]);
    });

    socketInstance.on("disconnect", () => {
      console.log("Socket.IO disconnected");
    });

    setSocket(socketInstance);

    return () => {
      if (socketInstance) {
        socketInstance.disconnect();
      }
    };
  }, []);

  const handleSendMessage = () => {
    if (newMessage.trim() === "" || !selectedUser) return;

    const messageData = {
      to_user_id: selectedUser.id,
      content: newMessage,
    };

    socket.emit("send_message", messageData);

    setMessages((prevMessages) => [
      ...prevMessages,
      { from_user_id: "me", content: newMessage },
    ]);
    setNewMessage("");
  };

  return (
    <div>
      <div className="user-list">
        <h2>Select a User to Chat</h2>
        <div>test str 8</div>
        <ul>
          {users.map((user) => (
            <li
              key={user.id}
              onClick={() => setSelectedUser(user)}
              style={{ cursor: "pointer" }}
            >
              <img src={userDefaultPfp} alt="User" className="user-avatar" />
              <span>{user.name}</span>
            </li>
          ))}
        </ul>
      </div>

      {selectedUser && (
        <div className="chat-box">
          <div className="chat-header">
            <h3>Chat with {selectedUser.name}</h3>
          </div>

          <div className="messages">
            {messages.map((message, index) => (
              <div key={index} className="message">
                <strong>
                  {message.from_user_id === "me" ? "You" : "Other"}
                </strong>
                : {message.content}
              </div>
            ))}
          </div>

          <div className="message-input">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;
