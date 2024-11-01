import { useState, useEffect } from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Form/Login/Login";
import Register from "./components/Form/Register/Register";
import Order from "./components/Home/Order/Order"
import Home from "./components/Home/Home";
import MyProfile from "./components/Home/MyProfile/MyProfile";

export default function App() {
  const [token, setToken] = useState();

  useEffect(() => {
    const auth = localStorage.getItem("access_token");
    if (auth) {
      setToken(auth);
    }
  }, []);

  return (
    <Router>
      <Routes>
        {/* Routes for pages available without authorization */}
        {!token && (
          <>
            <Route path="/login" element={<Login></Login>}></Route>
            <Route path="/register" element={<Register></Register>}></Route>   {/* <Route path="register" element={<Register></Register>}></Route> ???*/}
            <Route
              path="*"
              element={<Navigate to={"/login"}></Navigate>}
            ></Route>
          </>
        )}

        {/* Routes for pages available with authorization */}
        {token && (
          <>
            <Route path="/" element={<Home />}></Route>
            <Route path="/orders" element={<Order />}></Route>
            <Route path="/myprofile" element={<MyProfile />}></Route>
            {/* Redirect to / if logged in */}
            <Route path="*" element={<Navigate to={"/"} />}></Route>
          </>
        )}
      </Routes>
    </Router>
  );
}
