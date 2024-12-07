import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import axios from "axios";
import userDefaultPfp from "../../../assets/images/userDefaultPfp.png";
import "./Chat.css";

const Chat = () => {
  console.log("here -1");
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [socket, setSocket] = useState(null);
  const [userId, setUserId] = useState(null); 
  console.log("here 0");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get("http://localhost:8006/users/all");
        console.log("here 1");
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, []);
  
  useEffect(() => {
    const fetchUserData = async () => {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        console.error("Access token is missing");
        return;
      }
      try {
        const response = await axios.get("http://localhost:8005/users/me", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        console.log("Current user data:", response.data);
        setUserId(response.data.id);  // Set the user ID
      } catch (error) {
        console.error("Error fetching current user data:", error);
      }
    };

    fetchUserData();
  }, []);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    console.log("here 2");
    if (!accessToken) {
      console.error("Access token is missing");
      return;
    }
    console.log("here 3");
    const socketInstance = io("http://localhost:8009", {
      path: "/sockets",
      extraHeaders: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    console.log("socket instance:", socketInstance);

    console.log("here 4");
    socketInstance.on("connect", () => {
      console.log("Connected to Socket.IO!");
    });

    socketInstance.on("receive_message", (message) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { from_user_id: message.from_user_id, content: message.content },
      ]);
      console.log("here 9");
    });
    console.log("here 5");

    socketInstance.on("disconnect", () => {
      console.log("Socket.IO disconnected");
    });

    setSocket(socketInstance);

    return () => {
      console.log("here 6");
      if (socketInstance) {
        socketInstance.disconnect();
      }
    };
  }, []);

  const handleSendMessage = async () => {
    console.log("here 7");
    if (newMessage.trim() === "" || !selectedUser || !userId) return; 

    const messageData = {
      from_user_id: userId, 
      to_user_id: selectedUser.id,
      content: newMessage,
    };

    console.log("Emitting send_message with data:", messageData);
    console.log("socket:", socket);

    socket.emit("send_message", messageData);

    console.log("emitted");

    setMessages((prevMessages) => [
      ...prevMessages,
      { from_user_id: userId, content: newMessage }, 
    ]);
    setNewMessage("");
    console.log("here 8");
  };

  return (
    <div>
      <div className="user-list">
        <h2>Select a User to Chat</h2>
        <div>test str 10</div>
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
                  {message.from_user_id === userId ? "You" : "Other"}
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
