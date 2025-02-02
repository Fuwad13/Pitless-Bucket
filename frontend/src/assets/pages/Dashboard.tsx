import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Home, Menu, Settings } from "lucide-react";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import FileCard from "../customComponents/FileCard";
import FileUpload from "../modals/FileUpload";
import useAxiosPublic from "../hooks/AxiosPublic";

interface FileType {
  name: string;
  type: string;
}

const Dashboard: React.FC = () => {
  const axiosPublic = useAxiosPublic();
  const [files, setFiles] = useState<FileType[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const useFetchFiles = () => {
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await axiosPublic("/api/files");

          if (!response) {
            throw new Error("Failed to fetch files");
          }

          console.log("Files fetched successfully:", response.data.files);
          setFiles(response.data.files);
        } catch (error) {
          setError((error as Error).message);
          console.error("Error fetching files:", error);
        } finally {
          setLoading(false);
        }
      };

      fetchData();
    }, []);

    return { files, error, loading };
  };
  const handleDownload = async (file: FileType) => {
    try {
      const response = await axiosPublic.get("/api/get_file", {
        params: { file_name: file.name },
        responseType: "blob",
      });

      const blob = new Blob([response.data]);

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      window.URL.revokeObjectURL(url);
      console.log(`Downloaded: ${file.name}`);
      toast.success("File downloaded successfully!", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
    } catch (error) {
      console.error("Download error:", error);
      toast.error("Failed to download file!", {
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

  useFetchFiles();
  return (
    <div className="flex min-h-screen">
      {/* Sidebar for Large Screens, we see this at desktop*/}
      <aside className="hidden md:flex flex-col w-64 bg-blue-50 p-6 space-y-4 shadow-lg">
        <h2 className="text-2xl font-bold text-blue-600">Pitless Bucket</h2>
        <nav className="space-y-3">
          <FileUpload />
          <Link
            to="/dashboard"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Home size={20} /> Home
          </Link>

          <Link
            to="/settings"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Settings size={20} /> Settings
          </Link>
        </nav>
      </aside>

      {/* Mobile Sidebar (Drawer) needs come position fixing for drop down icon, can just move it to navbar later*/}
      <Sheet>
        <SheetTrigger asChild>
          <Button className="md:hidden absolute top-4 left-4">
            <Menu />
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="space-y-4">
            <FileUpload />
            <Link
              to="/dashboard"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Home size={20} /> Home
            </Link>

            <Link
              to="/settings"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Settings size={20} /> Settings
            </Link>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main Content section */}
      <main className="flex-1 p-6 bg-gray-100">
        <h1 className="text-3xl font-bold text-gray-900">
          Your Files & Folders
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          {loading ? (
            <p>Loading files...</p>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            files.map((file) => (
              <FileCard key={file.id} file={file} onDownload={handleDownload} />
            ))
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
