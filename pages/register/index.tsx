  import axios from "axios";
  import { useState } from "react";
  import { setTokenAndRedirect } from "../common";
  import React from "react";
  import { registerService } from "@/services";

  import "./style.css";
  import { Link } from "react-router-dom";
  import { showToast } from "@/utils/toast";

  const RegisterForm = () => {
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = async (event) => {
      alert("registered successfully")
      event.preventDefault();
      const formData = new FormData(event.target);
      const email = formData.get("email");
      const password = formData.get("password");

      const input = { fullName, email, password };
      try{
      const response = await registerService(input);
      console.log("Registration response:", response); // Log the response

      const { status, cls, msg } = response;
      showToast(msg, cls);
      

      if (!status) {
        return;
      }

      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);
    } catch (error) {
      console.error("Error during registration:", error); // Log the error
      const message = error.response?.data?.msg || "An unexpected error occurred.";
      
    }
  }
    

    return (
      <div className="register-form">
        <form onSubmit={handleSubmit}>
          <h2>Register</h2>
          <p className="text-secondary text-center">
            Welcome to Meetup! Register to create an account.
          </p>
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              type="text"
              name="fullName"
              id="fullName"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              name="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button className="register-btn" type="submit">
            Register
          </button>
          Already Have an Account?{" "}
          <Link className="login-link" to="/login">
            Login here
          </Link>
        </form>
      </div>
    );
  };

  const RegisterPage = () => {
    return (
      <main className="register-page">
        <RegisterForm />
      </main>
    );
  };

  export default RegisterPage;
