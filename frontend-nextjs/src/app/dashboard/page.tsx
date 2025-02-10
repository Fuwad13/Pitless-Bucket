"use client";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Home, Loader2, Menu, Settings } from "lucide-react";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { toast } from "react-toastify";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import useAxiosPublic from "@/hooks/use-axios";
import FileUpload from "@/modals/FileUpload";
import FileCard from "@/components/customComponents/FileCard";

interface FileType {
  uid: string;
  user_id: string;
  file_name: string;
  content_type: string;
  extension: string;
  size: number;
  created_at: Date;
  updated_at: Date;
}

const Dashboard: React.FC = () => {
  const axiosPublic = useAxiosPublic();
  const [files, setFiles] = useState<FileType[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const MySwal = withReactContent(Swal);

  // const fetchFiles = () => {
  //   useEffect(() => {
  //     const fetchData = async () => {
  //       try {
  //         const response = await axiosPublic("/api/files");

  //         if (!response) {
  //           throw new Error("Failed to fetch files");
  //         }
  //         setFiles(response.data.files);
  //       } catch (error) {
  //         setError((error as Error).message);
  //         console.error("Error fetching files:", error);
  //       } finally {
  //         setLoading(false);
  //       }
  //     };
  //     console.log("fetched", files);
  //     fetchData();
  //   }, []);

  //   return { files, error, loading };
  // };

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axiosPublic.get("/api/v1/drive/files");
        if (!response) {
          throw new Error("Failed to fetch files");
        }
        setFiles(response.data);
      } catch (error) {
        setError((error as Error).message);
        console.error("Error fetching files:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  const refreshFiles = async () => {
    try {
      const response = await axiosPublic.get("/api/v1/drive/files");
      setFiles(response.data);
    } catch (error) {
      setError((error as Error).message);
    } finally {
      setLoading(false);
    }
  };
  const handleDownload = async (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => {
    try {
      // const response = await axiosPublic.get("/api/get_file", {
      //   params: { file_id: file.uid },
      //   responseType: "blob",
      // });

      const downloadLink =
        axiosPublic.defaults.baseURL +
        "/api/v1/drive/download?file_id=" +
        file.uid;

      // const blob = new Blob([response.data]);

      // const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = downloadLink;
      a.download = file.file_name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      window.URL.revokeObjectURL(downloadLink);
      console.log(`Download Starting: ${file.uid} - ${file.file_name}`);
      toast.success("File download starting soon!", {
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

  const handleDelete = async (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => {
    const result = await MySwal.fire({
      title: "Are you sure?",
      text: "This action cannot be undone!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Yes, delete it!",
      cancelButtonText: "Cancel",
    });

    if (result.isConfirmed) {
      try {
        await axiosPublic.delete("/api/v1/drive/delete_file", {
          params: { file_id: file.uid },
        });

        setFiles((prevFiles) => prevFiles.filter((f) => f.uid !== file.uid));
        toast.success("File deleted successfully!", {
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
        console.error("Delete error:", error);
        toast.error("Failed to delete file!", {
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
    }
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar for Large Screens, we see this at desktop*/}
      <aside className="hidden md:flex flex-col w-52 bg-blue-50 p-6 space-y-4 shadow-lg border-r">
        {/* <h2 className="text-2xl font-bold text-blue-600">Pitless Bucket</h2> */}
        <nav className="space-y-3">
          <FileUpload refreshFiles={refreshFiles} />
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

      {/* Mobile Sidebar (Drawer) needs come position fixing for drop down icon, can just move it to navbar later*/}
      <Sheet>
        <SheetTrigger asChild>
          <Button className="md:hidden absolute top-4 left-4">
            <Menu />
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="space-y-4">
            <FileUpload refreshFiles={refreshFiles} />
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
        </SheetContent>
      </Sheet>

      {/* Main Content section */}
      <main className="flex-1 p-6 bg-gray-100">
        <h1 className="text-3xl font-bold text-gray-900">
          Your Files & Folders
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          {loading ? (
            <div className="min-h-screen flex justify-center items-center col-span-3">
              <div className="flex flex-col-reverse items-center justify-center gap-2">
                <p>Loading files</p>
                <Loader2 className="w-6 h-6 animate-spin text-gray-500" />
              </div>
            </div>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            files.map((file) => (
              <FileCard
                key={file.uid}
                file={file}
                onDownload={handleDownload}
                onDelete={handleDelete}
              />
            ))
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
