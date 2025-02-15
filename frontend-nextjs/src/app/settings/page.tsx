"use client";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Home,
  Loader2,
  Menu,
  Settings,
  HardDrive,
  Cloud,
  Github,
  ArrowLeft,
} from "lucide-react";
import React, { useContext, useEffect, useState } from "react";
import Link from "next/link";
import { toast } from "react-toastify";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { AuthContext } from "@/app/AuthContext";
import { useRouter } from "next/navigation";
import useAxiosPublic from "@/hooks/use-axios";
import { headers } from "next/headers";
import { auth } from "../firebase";

const SettingsPage: React.FC = () => {
  const { currentUser, getIdToken } = useContext(AuthContext);
  const router = useRouter();
  const [loading, setLoading] = useState<boolean>(false);
  const MySwal = withReactContent(Swal);
  const axiosPublic = useAxiosPublic();

  useEffect(() => {
    if (!currentUser) {
      router.push("/login");
    }
  }, [currentUser, router]);

  const handleConnectGoogleDrive = async () => {
    const token = await getIdToken();

    try {
      const response = await axiosPublic.get("api/v1/auth/google", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const google_auth_url = response.data["google_auth_url"];
      window.open(
        google_auth_url,
        "GoogleAuth",
        "width=500,height=600,scrollbars=yes"
      );

      // toast.success("Google Drive connected successfully!", {
      //   position: "top-right",
      //   autoClose: 3000,
      //   hideProgressBar: false,
      //   closeOnClick: false,
      //   pauseOnHover: true,
      //   draggable: true,
      //   progress: undefined,
      //   theme: "dark",
      // });
    } catch (error) {
      console.error(error);
      toast.error("Failed to connect Google Drive", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
    }
  };

  const handleConnectOneDrive = () => {
    toast.success("OneDrive connected successfully!", {
      position: "top-right",
      autoClose: 3000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
    });
  };

  const handleConnectDropbox = () => {
    toast.success("Dropbox connected successfully!", {
      position: "top-right",
      autoClose: 3000,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
    });
  };
  const handleGoBack = () => {
    router.back();
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar for Large Screens */}
      <aside className="hidden md:flex flex-col w-52 bg-blue-50 p-6 space-y-4 shadow-lg border-r">
        <nav className="space-y-3">
          <Link
            href="/dashboard"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Home size={20} /> Home
          </Link>
          <Link
            href="/settings"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Settings size={20} /> Settings
          </Link>
        </nav>
      </aside>

      {/* Mobile Sidebar (Drawer) */}
      <Sheet>
        <SheetTrigger asChild>
          <Button className="md:hidden absolute top-4 left-4">
            <Menu />
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="space-y-4">
            <Link
              href="/dashboard"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Home size={20} /> Home
            </Link>
            <Link
              href="/settings"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Settings size={20} /> General Settings
            </Link>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main Content section */}
      <main className="flex-1 p-6 bg-gray-100">
        <div className="flex items-center gap-2 my-2">
          <button
            onClick={handleGoBack}
            className="flex items-center bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition duration-200"
          >
            <ArrowLeft className="w-5 h-5" />
            Go Back
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Storage Settings</h1>
        </div>

        {/* Add More Storage Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Add More Storage
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Google Drive Card */}
            <div
              className="flex flex-col items-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              onClick={handleConnectGoogleDrive}
            >
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png"
                alt="Google Drive"
                className="w-12 h-12 mb-4"
              />
              <h3 className="text-lg font-medium text-gray-700">
                Google Drive
              </h3>
              <p className="text-sm text-gray-500">
                Connect your Google Drive account
              </p>
            </div>

            {/* OneDrive Card */}
            <div
              className="flex flex-col items-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              onClick={handleConnectOneDrive}
            >
              <img src="drive.png" alt="OneDrive" className="w-24 h-12 mb-4" />
              <h3 className="text-lg font-medium text-gray-700">OneDrive</h3>
              <p className="text-sm text-gray-500">
                Connect your OneDrive account
              </p>
            </div>

            {/* Dropbox Card */}
            <div
              className="flex flex-col items-center p-6 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
              onClick={handleConnectDropbox}
            >
              <img src="dropbox.png" alt="Dropbox" className="w-12 h-12 mb-4" />
              <h3 className="text-lg font-medium text-gray-700">Dropbox</h3>
              <p className="text-sm text-gray-500">
                Connect your Dropbox account
              </p>
            </div>
          </div>
        </div>

        {/* Current Storage Section */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Current Storage
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <HardDrive className="text-blue-500" size={24} />
                <div>
                  <h3 className="text-lg font-medium text-gray-700">
                    Local Storage
                  </h3>
                  <p className="text-sm text-gray-500">500 MB of 1 GB used</p>
                </div>
              </div>
              <Button variant="outline" className="text-blue-600">
                Manage
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default SettingsPage;
