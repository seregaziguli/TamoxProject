import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./Header.css";
import userDefaultPfp from "../../../assets/images/userDefaultPfp.png";
import Chat from "../Chat/Chat";

export default function Header() {
  const [isPfpPopUpOpen, setIsPfpPopUpOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState(userDefaultPfp);
  const [isExitWindowOpen, setIsExitWindowOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const fetchUserId = async () => {
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        console.error("Access token not found");
        return;
      }

      try {
        const response = await axios.get("http://localhost:8005/users/me", {
          headers: {
            Authorization: `Bearer ${accessToken}`, 
          },
        });
        setUserId(response.data.id); 
      } catch (error) {
        console.error("Error fetching user ID:", error);
      }
    };

    fetchUserId();
  }, []);

  const handleExitClick = () => {
    setIsExitWindowOpen(true);
  };

  const handleMessagesClick = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <>
      <div className="header-wrapper bg-[#f8f8f8] h-24 w-full flex justify-between pr-20 pl-20 items-center space-x-10">
        <div>
          {userId ? (
            <div className="user-id-display">User ID: {userId}</div>
          ) : (
            <div className="user-id-loading">Loading user ID...</div>
          )}
        </div>

        <Link to={"/orders"}>
          <div>Make an order</div>
        </Link>

        <div className="header-user-pfp-container h-16 w-16 rounded-full bg-[#fff] flex justify-center relative">
          <img
            className="rounded-full cursor-pointer object-cover"
            src={imageUrl}
            alt="User Profile"
            onError={(e) => (e.target.src = userDefaultPfp)}
            onClick={() => setIsPfpPopUpOpen(!isPfpPopUpOpen)}
            style={{
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          />
        </div>

        {isPfpPopUpOpen && (
          <div
            className="pop-up-on-pfp absolute right-12 h-auto w-auto 
                bg-[#ececec] pt-4 pb-4 pl-4 pr-4 rounded-lg flex 
                items-center justify-center text-center z-10"
          >
            <div className="">
              <Link to="/myprofile">
                <div className="mb-4 cursor-pointer">My Profile</div>
              </Link>

              <Link to="/">
                <div className="mb-4 cursor-pointer">Notifications</div>
              </Link>

              <Link to="#" onClick={handleMessagesClick}>
                <div className="mb-4 cursor-pointer">Messages</div>
              </Link>

              <Link to="/">
                <div className="mb-4 cursor-pointer">Settings</div>
              </Link>

              <p className="mb-4 cursor-pointer" onClick={handleExitClick}>
                Exit
              </p>
            </div>
          </div>
        )}
      </div>

      {isChatOpen && <Chat />}
    </>
  );
}
