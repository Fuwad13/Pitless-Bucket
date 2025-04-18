"use client";

import React, { useContext, useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Settings, Menu, Info, HardDrive } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import FileUpload from "@/modals/FileUpload";
import { AuthContext } from "@/app/AuthContext";
import useAxiosPublic from "@/hooks/AxiosPublic";

interface SidebarProps {
  refreshFiles: () => void;
}
interface StorageStat {
  used: number;
  available: number;
  total: number;
}

const Sidebar: React.FC<SidebarProps> = ({ refreshFiles }) => {
  const pathname = usePathname();
  console.log(pathname);
  const { getIdToken } = useContext(AuthContext)!;
  const [storageStat, setStorageStat] = useState<StorageStat>({
    used: 0,
    available: 0,
    total: 0,
  });
  const axiosPublic = useAxiosPublic();
  useEffect(() => {
    fetchStorageStat();
  }, []);

  const fetchStorageStat = async () => {
    try {
      const token = await getIdToken();
      const response = await axiosPublic.get(
        "/api/v1/file_manager/storage_usage",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setStorageStat(response.data);
    } catch (error) {
      console.error("Error fetching storage stat:", error);
    }
  };

  const formatSize = (size: number): string => {
    if (size === 0) return "0 Bytes";

    const units = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const formattedSize = (size / Math.pow(1024, i)).toFixed(2);

    return `${formattedSize} ${units[i]}`;
  };
  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-52 bg-blue-50 p-6 space-y-4 shadow-lg border-r">
        <nav className="space-y-3">
          {pathname === "/dashboard" && (
            <FileUpload refreshFiles={refreshFiles} />
          )}

          {/* Navigation Links */}
          <Link
            href="/dashboard"
            className={`flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200 ${
              pathname === "/dashboard" ? "text-blue-600 font-semibold" : ""
            }`}
          >
            <Home size={20} /> Home
          </Link>

          <Link
            href="/settings"
            className={`flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200 ${
              pathname === "/settings" ? "text-blue-600 font-semibold" : ""
            }`}
          >
            <Settings size={20} /> Settings
          </Link>

          {pathname === "/settings" && (
            <Link
              href="/about"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200"
            >
              <Info size={20} /> About
            </Link>
          )}
        </nav>
        <div className="flex items-center gap-3 fixed bottom-[30px] left-3">
          <HardDrive className="text-blue-500" size={24} />
          <div>
            <h3 className="text-lg font-medium text-gray-700">Storage</h3>
            <p className="text-sm text-gray-500">
              {formatSize(storageStat.used)} of {formatSize(storageStat.total)}{" "}
              used
            </p>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar (Drawer/Sheet) */}
      <Sheet>
        <SheetTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            className="md:hidden fixed top-4 left-4 z-50"
          >
            <Menu className="h-5 w-5" />
            <span className="sr-only">Open menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-[250px] sm:w-[300px] p-6">
          <nav className="space-y-4 flex flex-col h-full">
            {pathname === "/dashboard" && (
              <FileUpload refreshFiles={refreshFiles} />
            )}

            {/* Navigation Links */}
            <Link
              href="/dashboard"
              className={`flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200 py-2 ${
                pathname === "/dashboard" ? "text-blue-600 font-semibold" : ""
              }`}
            >
              <Home size={20} /> Home
            </Link>

            <Link
              href="/settings"
              className={`flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200 py-2 ${
                pathname === "/settings" ? "text-blue-600 font-semibold" : ""
              }`}
            >
              <Settings size={20} /> Settings
            </Link>

            {/* Conditionally render About link only on /settings */}
            {pathname === "/settings" && (
              <Link
                href="/about"
                className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors duration-200 py-2"
              >
                <Info size={20} /> About
              </Link>
            )}
          </nav>
        </SheetContent>
      </Sheet>
    </>
  );
};

export default Sidebar;
