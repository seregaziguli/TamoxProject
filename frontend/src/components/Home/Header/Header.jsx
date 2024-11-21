import React from "react";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Header.css";
import axios from "axios";
import userDefaultPfp from "../../../assets/images/userDefaultPfp.png";
import logo from "../../../assets/images/logo.png";

export default function Header() {
  const [isPfpPopUpOpen, setIsPfpPopUpOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState(userDefaultPfp);
  const [isExitWindowOpen, setIsExitWindowOpen] = useState(false);

  const handleExitClick = () => {
    setIsExitWindowOpen(true);
  };

  return (
    <>
      <div className="header-wrapper bg-[#f8f8f8] h-24 w-full flex justify-between pr-20 pl-20 items-center space-x-10">
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

              <Link to="/">
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
    </>
  );
}
