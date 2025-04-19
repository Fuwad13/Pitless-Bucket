"use client";
import { Button } from "@/components/ui/button";
import { Grid, List, Loader2 } from "lucide-react";
import React, { useContext, useEffect, useState } from "react";
import { toast } from "react-toastify";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import useAxiosPublic from "@/hooks/use-axios";
import FileCard from "@/components/customComponents/FileCard";
import { AuthContext } from "@/app/AuthContext";
import { useRouter } from "next/navigation";
import SearchBar from "@/components/customComponents/SearchBar";
import FileTable from "@/components/customComponents/FileTable";
import RenameModal from "@/modals/RenameModal";
import Sidebar from "@/components/customComponents/Sidebar";

interface FileType {
  uid: string;
  firebase_uid: string;
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
  const [filteredFiles, setFilteredFiles] = useState<FileType[]>([]);
  const { currentUser, getIdToken } = useContext(AuthContext)!;
  const [layoutMode, setLayoutMode] = useState<"card" | "table">("card");
  const [renameModalOpen, setRenameModalOpen] = useState(false);
  const [fileToRename, setFileToRename] = useState<FileType | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (!currentUser) {
      router.push("/login");
      return;
    }
    const fetchFiles = async () => {
      try {
        const token = await getIdToken();
        console.log("Token:", token); // for debugging
        const response = await axiosPublic.get(
          "/api/v1/file_manager/list_files",
          { headers: { Authorization: `Bearer ${token}` } }
        );
        if (!response) {
          throw new Error("Failed to fetch files");
        }
        setFiles(response.data);
        setFilteredFiles(response.data);
      } catch (error) {
        setError((error as Error).message);
        console.error("Error fetching files:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [router, currentUser, axiosPublic, getIdToken]);

  const refreshFiles = async () => {
    try {
      const token = await getIdToken();
      const response = await axiosPublic.get(
        "/api/v1/file_manager/list_files",
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setFiles(response.data);
      setFilteredFiles(response.data);
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
      const response = await axiosPublic.get(
        "/api/v1/file_manager/download_file",
        {
          params: { file_id: file.uid },
          responseType: "blob",
          headers: { Authorization: `Bearer ${await getIdToken()}` },
        }
      );

      const blob = new Blob([response.data]);

      const downloadLink = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = downloadLink;
      a.download = `${file.file_name}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      window.URL.revokeObjectURL(downloadLink);
      console.log(`Download Starting: ${file.uid} - ${file.file_name}`);
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
        const token = await getIdToken();
        await axiosPublic.delete("/api/v1/file_manager/delete_file", {
          params: { file_id: file.uid },
          headers: { Authorization: `Bearer ${token}` },
        });

        setFiles((prevFiles) => prevFiles?.filter((f) => f.uid !== file.uid));
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

  const handleEdit = (file: FileType) => {
    setFileToRename(file);
    setRenameModalOpen(true);
  };

  const handleSearch = (query: string) => {
    const lowerCaseQuery = query.toLowerCase();
    const filtered = files?.filter((file) =>
      file.file_name.toLowerCase().includes(lowerCaseQuery)
    );
    setFilteredFiles(filtered);
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar for Large Screens, we see this at desktop*/}
      {/* <aside className="hidden md:flex flex-col w-52 bg-blue-50 p-6 space-y-4 shadow-lg border-r">
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
      </aside> */}

      {/* Mobile Sidebar (Drawer) needs come position fixing for drop down icon, can just move it to navbar later*/}
      {/* <Sheet>
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
      </Sheet> */}
      <Sidebar refreshFiles={refreshFiles} />

      {/* Main Content section */}
      <main className="flex-1 p-6 bg-gray-100 overflow-x-auto">
        <div className="flex flex-col justify-center items-center gap-4">
          <h1 className="text-3xl font-bold text-gray-900 text-center">
            Your Files & Folders
          </h1>

          <div className="w-full max-w-2xl flex justify-center gap-4">
            <SearchBar onSearch={handleSearch} />
            <Button
              className="mt-1"
              variant="outline"
              size="icon"
              onClick={() =>
                setLayoutMode(layoutMode === "card" ? "table" : "card")
              }
              title={
                layoutMode === "card"
                  ? "Switch to Table View"
                  : "Switch to Card View"
              }
            >
              {layoutMode === "card" ? <List size={24} /> : <Grid size={24} />}
            </Button>
          </div>
        </div>
        <div className="mt-6">
          {loading ? (
            <div className="min-h-screen flex justify-center items-center col-span-3">
              <div className="flex flex-col-reverse items-center justify-center gap-2">
                <p>Loading files</p>
                <Loader2 className="w-6 h-6 animate-spin text-gray-500" />
              </div>
            </div>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : Array.isArray(filteredFiles) && filteredFiles.length > 0 ? (
            layoutMode === "card" ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredFiles?.map((file) => (
                  <FileCard
                    key={file.uid}
                    file={file}
                    onDownload={handleDownload}
                    onDelete={handleDelete}
                    refreshFiles={refreshFiles}
                  />
                ))}
              </div>
            ) : (
              <FileTable
                files={filteredFiles}
                onDownload={handleDownload}
                onDelete={handleDelete}
                onEdit={handleEdit}
              />
            )
          ) : (
            <p className="col-span-3 text-center text-gray-500">
              No files found matching your search.
            </p>
          )}
        </div>
        {renameModalOpen && fileToRename && (
          <RenameModal
            file={fileToRename}
            isOpen={renameModalOpen}
            onClose={() => setRenameModalOpen(false)}
            refreshFiles={refreshFiles}
          />
        )}
      </main>
    </div>
  );
};

export default Dashboard;
