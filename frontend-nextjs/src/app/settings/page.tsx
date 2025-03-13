"use client";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Home,
  Menu,
  Settings,
  HardDrive,
  ArrowLeft,
  Loader2,
} from "lucide-react";
import React, { useContext, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { toast } from "react-toastify";
import { AuthContext } from "@/app/AuthContext";
import { useRouter } from "next/navigation";
import useAxiosPublic from "@/hooks/use-axios";
import { Input } from "@/components/ui/input";

interface StorageStat {
  used: number;
  available: number;
  total: number;
}

const SettingsPage: React.FC = () => {
  const { currentUser, getIdToken } = useContext(AuthContext);
  const router = useRouter();
  const [loading, setLoading] = useState<boolean>(false);
  const axiosPublic = useAxiosPublic();
  const [error, setError] = useState<string | null>(null);
  const [storageStat, setStorageStat] = useState<StorageStat>({
    used: 0,
    available: 0,
    total: 0,
  });
  const [telegramUserId, setTelegramUserId] = useState("");
  const hasFetchedStorageStat = useRef(false);

  useEffect(() => {
    if (!currentUser) {
      router.push("/login");
    } else if (!hasFetchedStorageStat.current) {
      fetchStorageStat();
      hasFetchedStorageStat.current = true;
    }
  }, [currentUser, router]);

  const fetchStorageStat = async () => {
    try {
      setLoading(true);
      const token = await getIdToken();
      const response = await axiosPublic.get(
        "/api/v1/file_manager/storage_usage",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStorageStat(response.data);
      console.log("Storage Stat:", response.data);
    } catch (error) {
      setError((error as Error).message);
      console.error("Error fetching storage stat:", error);
    } finally {
      setLoading(false);
    }
  };
  const HandleConnectTelegram = async () => {
    console.log("connect TG!");
  };

  const handleConnectGoogleDrive = async () => {
    const token = await getIdToken();

    try {
      const response = await axiosPublic.get("/api/v1/auth/google", {
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

  const formatSize = (size: number): string => {
    if (size === 0) return "0 Bytes";

    const units = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const formattedSize = (size / Math.pow(1024, i)).toFixed(2);

    return `${formattedSize} ${units[i]}`;
  };

  const handleConnectDropbox = async () => {
    const token = await getIdToken();

    try {
      const response = await axiosPublic.get("/api/v1/auth/dropbox", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const dropbox_auth_url = response.data["dropbox_auth_url"];
      window.open(
        dropbox_auth_url,
        "DropboxAuth",
        "width=500,height=600,scrollbars=yes"
      );

      // toast.success("Dropbox connected successfully!", {
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
      toast.error("Failed to connect Dropbox", {
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
  const handleGoBack = () => {
    router.back();
  };

  // telegram handle functions
  const handleInputChange = (event) => {
    setTelegramUserId(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const token = await getIdToken();
    const response = await axiosPublic.post(
      `/api/v1/auth/link_telegram?tg_id=${telegramUserId}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    console.log(response);
    console.log("Connecting to Telegram User ID:", telegramUserId);
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

        {/* Connect ohter accounts */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Connect other accounts
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Telegram */}
            <div className="flex flex-col gap-2 p-6 border bg-white rounded-lg shadow-sm transition-shadow">
              <div className="flex gap-4 items-center">
                <img
                  src="https://upload.wikimedia.org/wikipedia/commons/8/83/Telegram_2019_Logo.svg"
                  alt="Telegram"
                  className="w-12 h-12"
                />
                <div>
                  <h3 className="text-lg font-medium text-gray-700">
                    Telegram
                  </h3>
                  <p className="text-sm text-gray-500">Connect your account</p>
                </div>
              </div>
              {/* add connected status later */}
              {
                // telegramUserId ?
                <form onSubmit={handleSubmit} className="flex gap-2 mt-4">
                  <Input
                    type="text"
                    placeholder="Enter Telegram User ID"
                    onChange={handleInputChange}
                    className="flex-1"
                  />
                  <Button
                    variant="default"
                    className="ml-auto bg-blue-600 hover:bg-blue-700"
                  >
                    Connect
                  </Button>
                </form>
                // : (
                //   <div>Not connected</div>
                // )
              }
            </div>
          </div>
        </div>

        {/* Current Storage Section */}

        {loading ? (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex flex-col-reverse items-center justify-center gap-2">
              <p>Loading Storage Usage</p>
              <Loader2 className="w-6 h-6 animate-spin text-gray-500" />
            </div>
          </div>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
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
                      Storage
                    </h3>
                    <p className="text-sm text-gray-500">
                      {formatSize(storageStat.used)} of{" "}
                      {formatSize(storageStat.total)} used
                    </p>
                  </div>
                </div>
                <Button variant="outline" className="text-blue-600">
                  Manage
                </Button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default SettingsPage;
