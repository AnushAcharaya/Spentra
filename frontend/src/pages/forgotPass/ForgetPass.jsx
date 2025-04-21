import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "./Input";
import Button from "./Button";

const ForgetPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  // Email validation pattern
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!emailPattern.test(email)) {
      setError("Please enter a valid email address");
      return;
    }

    setError("");
    setLoading(true);
    const api_url = "https://your-api-endpoint.com"; // Replace with actual API

    try {
      const response = await fetch(`${api_url}/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      setMessage(
        response.ok
          ? "Instructions sent to your email for resetting password"
          : data.message || "Something went wrong"
      );
    } catch (error) {
      setMessage("Failed to connect to the server. Please try again later.");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col md:flex-row items-center justify-center min-h-screen bg-white">
      {/* Left Section */}
      <section
        className="flex justify-center gap-5 md:flex w-1/2 h-screen bg-cover bg-center items-center  rounded-r-4xl"
        style={{ backgroundImage: "url('/bgImage.png')" }}
      >
        <div className="flex flex-col justify-center items-center h-full text-white text-center">
          <p className="text-4xl lg:text-5xl">Reset your</p>
          <p className="text-6xl lg:text-7xl font-bold">Spentra</p>
          <p className="text-4xl lg:text-5xl">Password for</p>
          <p className="text-4xl lg:text-5xl">Account Access</p>
        </div>
      </section>

      {/* Right Section */}
      <section className="flex flex-col items-center justify-center w-full md:w-1/2 px-6 py-8 md:py-0">
        <img
          src="/logo.png"
          alt="Logo"
          className="w-24 h-24 md:w-32 md:h-32 mb-4"
        />
        <div className="w-full max-w-md bg-[#a9f1ab] shadow-lg rounded-3xl p-6 text-center">
          <h2 className="uppercase font-bold text-2xl md:text-3xl">
            Forgot Password
          </h2>
          <p className="text-sm text-gray-600 mt-2">
            No worries, we will send you instructions to reset your password.
          </p>

          {/* Input & Buttons */}
          <form className="flex flex-col gap-4 mt-6" onSubmit={handleSubmit}>
            <Input
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {error && <p className="text-red-500 text-xs">{error}</p>}

            <Button
              onClick={() => navigate("/login/resetPass")}
              value="Reset Password"
              btn_type="gradient_btn"
            />
            <Button
              value="Back"
              btn_type="white_btn"
              onClick={() => navigate("/login")}
            />
          </form>

          {/* Loading & Messages */}
          {loading && <p className="text-gray-600 mt-2">Loading...</p>}
          {message && <p className="text-green-600 mt-2">{message}</p>}
        </div>
      </section>
    </div>
  );
};

export default ForgetPassword;
