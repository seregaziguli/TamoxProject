import React from "react";
import userDefaultPfp from "../../assets/images/userDefaultPfp.png";
import { useState } from "react";
import { Link } from "react-router-dom";
import Header from "./Header/Header";
import MainContent from "./MainContent/MainContent";


export default function Home(props) {
  return (
    <>
      <Header {...props}></Header>
      <MainContent></MainContent>
    </>
  );
}
