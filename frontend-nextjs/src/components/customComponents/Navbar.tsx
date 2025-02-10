"use client";
import { AuthContext } from "../../auth/AuthContext";
import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { signOut } from "firebase/auth";
import { getAuth } from "firebase/auth";
import { LogOut } from "lucide-react";
import { toast } from "react-toastify";

const Navbar: React.FC = () => {
  const { currentUser } = useContext(AuthContext);
  const auth = getAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate("/login");
      setIsDropdownOpen(false);
      toast.success("Logged out successfully!");
    } catch (error) {
      console.error("Error logging out:", error);
      setIsDropdownOpen(false);
    }
  };

  return (
    <header className="bg-blue-600 text-white">
      <div className="flex justify-between items-center p-4">
        <Link
          to="/dashboard"
          className="ml-14 md:ml-0 text-2xl font-bold text-white"
        >
          Pitless Bucket
        </Link>
        <nav className="flex items-center space-x-4">
          {currentUser && (
            <div className="relative">
              <div
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="rounded-full w-10 h-10 cursor-pointer"
              >
                <img
                  className="rounded-full w-10 h-10"
                  title={currentUser?.displayName || "user"}
                  src={
                    currentUser.photoURL ||
                    "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg"
                  }
                  alt={currentUser?.displayName || "User Photo"}
                />
              </div>
              {isDropdownOpen && (
                <div className="absolute right-0 mt-2 bg-white text-black shadow-md rounded-lg p-2 w-48 z-50">
                  <h5 className="p-4 text-gray-600">
                    {currentUser?.displayName || "User"}
                  </h5>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 flex items-center space-x-2"
                  >
                    <LogOut className="w-5 h-5 text-red-500" />{" "}
                    <span className="text-red-500">Logout</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
