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
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        console.log("fetching list of users...");
        const response = await axios.get("http://localhost:8006/users/all");
        setUsers(response.data);
        console.log("users fetched successfully:", response.data);
      } catch (error) {
        console.log("Failed to fetch users:", error);
      }
    };

    fetchUsers();
  }, []);

  useEffect(() => {
    const fetchUserData = async () => {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        console.log("access token is missing in local storage.");
        return;
      }
      try {
        console.log("fetching current user data...");
        const response = await axios.get("http://localhost:8005/users/me", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setUserId(response.data.id);
        console.log("current user data fetched successfully:", response.data);
      } catch (error) {
        console.log("Failed to fetch current user data:", error);
      }
    };

    fetchUserData();
  }, []);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      console.log("access token is missing in local storage.");
      return;
    }

    console.log("connecting to socket.io server");
    const socketInstance = io("http://localhost:8009", {
      path: "/sockets",
      extraHeaders: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    socketInstance.on("connect", () => {
      console.log("successfully connected to socket.io server.");
    });

    socketInstance.on("receive_message", (message) => {
      console.log("new message received:", message);
      setMessages((prevMessages) => [
        ...prevMessages,
        { from_user_id: message.from_user_id, content: message.content },
      ]);
    });

    socketInstance.on("disconnect", () => {
      console.log("disconnected from socket.io server.");
    });

    setSocket(socketInstance);

    return () => {
      console.log("disconnecting from socket.io server...");
      if (socketInstance) {
        socketInstance.disconnect();
      }
    };
  }, []);

  const handleSendMessage = async () => {
    if (newMessage.trim() === "" || !selectedUser || !userId) {
      console.log(
        "message sending failed: Missing data (message, selected user, or userId)."
      );
      return;
    }

    const messageData = {
      from_user_id: userId,
      to_user_id: selectedUser.id,
      content: newMessage,
    };

    console.log("socket:", socket)
    console.log("sending message:", messageData);

    socket.emit("send_message", messageData, (response) => {
      console.log("server response for send_message:", response);
    });

    console.log("message has been sent")

    setMessages((prevMessages) => [
      ...prevMessages,
      { from_user_id: userId, content: newMessage },
    ]);
    setNewMessage("");
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
