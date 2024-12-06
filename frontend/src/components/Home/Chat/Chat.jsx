import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import userDefaultPfp from "../../../assets/images/userDefaultPfp.png";
import "./Chat.css";

const Chat = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const ws = useRef(null);
  const navigate = useNavigate();

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
    if (selectedUser) {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        console.error("Access token is missing");
        return;
      }

      const socketUrl = `ws://localhost:8009/chat/ws/chat?access_token=${accessToken}`;
      console.log("access token:", accessToken);
      
      ws.current = new WebSocket(socketUrl);

      ws.current.onopen = () => {
        console.log("Connected to WebSocket!");
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessages((prevMessages) => [
          ...prevMessages,
          { from_user_id: message.from_user_id, content: message.content },
        ]);
      };

      return () => {
        if (ws.current) {
          ws.current.close();
        }
      };
    }
  }, [selectedUser]);

  const handleSendMessage = () => {
    if (newMessage.trim() === "" || !selectedUser) return;

    const messageData = {
      to_user_id: selectedUser.id,
      content: newMessage,
    };

    ws.current.send(JSON.stringify(messageData));
    setNewMessage("");
  };

  return (
    <div>
      <div className="user-list">
        <h2>Select a User to Chat</h2>
        <div>test str</div>
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
                  {message.from_user_id === selectedUser.id ? "You" : "Other"}
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
