import React, { useState } from "react";
//import { useNavigate } from "react-router-dom";
import Google from "../assets/google.png";

export default function Login() {
  return (
    <div className="w-full flex">
      {/* Left Section */}
      <div className="w-1/2 bg-white flex flex-col justify-center items-center p-10">
        <img src="/logo.png" alt="SpenTra Logo" className="w-40 mb-4" />
        <h2 className="text-2xl font-bold mb-4">LOGIN</h2>

        <form className="w-3/4">
          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 mb-4 border rounded-md"
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 mb-2 border rounded-md"
          />

          {/* Forgot Password Link */}
          <p
            className="text-right text-sm text-green-500 mb-4 cursor-pointer"
            onClick={() => navigate("/forgot-password")}
          >
            Forgot your password?
          </p>
          <button
            type="submit"
            className="w-full p-3 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600"
          >
            Login
          </button>
          <p className="text-center text-sm mt-4">Login with Others</p>
          <button
            type="button"
            className="w-full p-3 mt-2 bg-gray-200 text-black font-semibold rounded-lg shadow-md hover:bg-gray-300 flex items-center justify-center"
          >
            <img src={Google} alt="Google Icon" className="w-5 mr-2" />
            Login with Google
          </button>
        </form>
      </div>

      {/* Right Section */}
      <section className="bg-[url('./bgImage.png')] h-[100vh] w-1/2 bg-cover bg-center flex items-center flex-col pt-15 gap-8">
        <p className="text-white text-3xl font-bold mb-4">New to </p>
        <p className="text-white text-4xl font-bold">SPENTRA?</p>
        <div>
          <p className="text-white text-4xl font-bold text-center">
            Sign up today and take control of your financial journey.
          </p>
          <p className="text-white text-lg mt-2 text-center">
            Start tracking your expenses and unlock new possibilities
          </p>
        </div>
        <div className="flex justify-center flex-col gap-5">
          <hr className="w-130 text-white" />
          <button
            onClick={() => navigate("/signup")}
            className="mt-6 px-6 py-2 bg-white text-black font-semibold rounded-lg shadow-md hover:bg-gray-200"
          >
            Sign Up
          </button>
        </div>
      </section>
    </div>
  );
}
