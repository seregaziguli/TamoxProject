import "./Register.css";
import { useState, useEffect } from "react";
import { toast } from "react-toastify";
import { Link } from "react-router-dom";
import axios from "axios";

export default function Register() {
  const [formRegister, setFormRegister] = useState({
    name: "",
    email: "",
    password: "",
    phone_number: "",
  });

  const onChangeForm = (label, event) => {
    switch (label) {
      case "name":
        setFormRegister({ ...formRegister, name: event.target.value });
        break;

      case "email":
        // const email_validation = /\S+@\S+\.S+/;
        // if (email_validation.test(event.target.value)) {
        //   setFormRegister({ ...formRegister, email: event.target.value });
        // }
        setFormRegister({ ...formRegister, email: event.target.value });
        break;

      case "password":
        setFormRegister({ ...formRegister, password: event.target.value });
        break;

      case "phone_number":
        setFormRegister({ ...formRegister, phone_number: event.target.value });
        break;
    }
  };

  const onSubmitHandler = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8006/users", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(formRegister),
      });
      const data = await response.json();
      console.log(data);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <>
      <div className="register-form-container min-h-screen flex justify-center items-center">
        <div className="py-14 px-20 bg-white rounded-lg shadow-2xl z-20">
          <div>
            <h1 className="text-4xl font-bold mb-4 text-center cursor-pointer">
              Create an account
            </h1>
            <p
              className="w-96 text-center text-base mb-8 font-semibold text-gray-700 
                    tracking-wide cursor-pointer mx-auto"
            >
              Welcome to Amox
            </p>
          </div>
          <form onSubmit={onSubmitHandler}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Username"
                className="login-form-option block text-sm py-3 px-4 tracking-wider font-normal rounded-lg w-full border outline-none"
                onChange={(event) => {
                  onChangeForm("name", event);
                }}
              ></input>

              <input
                type="email"
                placeholder="Email"
                className="login-form-option block text-sm py-3 px-4 tracking-wider font-normal rounded-lg w-full border outline-none"
                onChange={(event) => {
                  onChangeForm("email", event);
                }}
              ></input>

              <input
                type="password"
                placeholder="Password"
                className="login-form-option block text-sm py-3 px-4 tracking-wider font-normal rounded-lg w-full border outline-none"
                onChange={(event) => {
                  onChangeForm("password", event);
                }}
              ></input>

              <input
                type="number"
                placeholder="Phone number"
                className="login-form-option block text-sm py-3 px-4 tracking-wider font-normal rounded-lg w-full border outline-none"
                onChange={(event) => {
                  onChangeForm("phone_number", event);
                }}
              ></input>
            </div>

            <div className="text-center mt-6">
              <button
                type="submit"
                className="py-3 w-64 text-xl text-white bg-gray-700 rounded-2xl hover:bg-gray-800 outline-none"
                onClick={() => {
                  toast.success(
                    "Successfully created account. \n You will now be redirected to the authorization page"
                  );
                }}
              >
                Create Account
              </button>

              <p className="mt-4 text-sm">
                Already have an account?{" "}
                <Link to="/signin">
                  <span className="underline cursor-pointer">Sign in</span>
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
