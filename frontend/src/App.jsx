import { useState, useEffect } from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Form/Login/Login.jsx";
import Register from "./components/Form/Register/Register.jsx";
import Home from "./components/Home/Home.jsx";
import MyProfile from "./components/Home/MyProfile/MyProfile.jsx";
import OrderForm from "./components/Home/OrderForm/OrderForm.jsx";

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
            <Route path="/orders" element={<OrderForm />}></Route>
            <Route path="/myprofile" element={<MyProfile />}></Route>
            {/* Redirect to / if logged in */}
            <Route path="*" element={<Navigate to={"/"} />}></Route>
          </>
        )}
      </Routes>
    </Router>
  );
}
