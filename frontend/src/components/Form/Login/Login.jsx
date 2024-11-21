import "./Login.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

export default function Login() {
  const [loginForm, setLoginForm] = useState({
    username: "",
    password: "",
  });

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setLoginForm({ ...loginForm, username: event.target.value });
        break;
      case "password":
        setLoginForm({ ...loginForm, password: event.target.value });
        break;
    }
  };

  const onSubmitHandler = async (e) => {
    e.preventDefault();
    console.log(loginForm);

    try {
      const response = await AuthService.login(
        loginForm.username,
        loginForm.password
      );
      console.log(response);

      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("token_type", response.data.token_type);

      setIsAuthenticated(true);
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
        navigate("/home")
        setTimeout(() => {
            setTimeout(() => {
                window.location.reload()
            }, 500)
        })
    }
  }, [isAuthenticated, navigate])

  const API_URL = "http://localhost:8005";

  const apiClient = axios.create({
    withCredentials: true,
    baseURL: API_URL,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  class AuthService {
    static async login(username, password) {
      return apiClient.post("users/login", { username, password });
    }
  }

  return (
    <>
      <div className="login-wrapper h-screen w-screen flex justify-center items-center space-x-3">
        <div className="login-left-container flex items-center justify-center"></div>

        <div className="login-right-container flex flex-col items-center justify-center">
          <div className="login-right-content">
            <div className="text-center">
              <div className="text-5xl font-bold">Welcome to Amox</div>
              <div className="text-lg font-medium mt-2">
                Please login into your account!
              </div>
            </div>

            <div className="w-full mt-24">
              <form onSubmit={onSubmitHandler}>
                <input
                  type="text"
                  placeholder="Email"
                  className="input-form-1 py-2 px-4 w-full mt-5"
                  onChange={(event) => {
                    onChangeForm("username", event);
                  }}
                ></input>

                <input
                  type="password"
                  placeholder="Password"
                  className="input-form-1 py-2 px-4 w-full mt-5"
                  onChange={(event) => {
                    onChangeForm("password", event);
                  }}
                ></input>

                <Link to="/forgot">
                  <div className="underline cursor-pointer text-end mt-2">
                    Forgot password?
                  </div>
                </Link>

                <button
                  type="submit"
                  className="login-submit-button py-2 w-full text-xl text-white outline-none mt-8"
                >
                  Sign in
                </button>
                <div className="line-or-line flex items-center justify-center space-x-3 mt-5">
                  <div className="line"></div>
                  <div className="or">or</div>
                  <div className="line"></div>
                </div>
                <div className="flex items-center justify-center mt-5">
                  <i className="fa-brands fa-google"></i>
                  <div className="ml-3">Sign in with google</div>
                </div>
                <div className="flex items-center justify-center mt-5">
                  Are you new?
                  <Link to="/register">
                    <span className="underline cursor-pointer ml-3">
                      Create an account
                    </span>
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
