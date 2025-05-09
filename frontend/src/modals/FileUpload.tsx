"use client";
import React, {
  useState,
  useCallback,
  useRef,
  useEffect,
  useContext,
} from "react";
import { Upload, Folder, File, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { toast } from "react-toastify";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import useAxiosPublic from "../hooks/AxiosPublic";
import { AuthContext } from "@/app/AuthContext";

interface FileUploadProps {
  refreshFiles: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ refreshFiles }) => {
  const [uploadType, setUploadType] = useState<"file" | "folder">("file");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const axiosPublic = useAxiosPublic();
  const { getIdToken } = useContext(AuthContext)!;

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFiles(Array.from(event.target.files));
    }
  };

  const handleDragEnter = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(true);
    },
    []
  );

  const handleDragLeave = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(false);
    },
    []
  );

  const handleDragOver = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
    },
    []
  );

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);

    const files = Array.from(event.dataTransfer.files);
    if (files.length > 0) {
      setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
    }
  }, []);

  const handleRemoveFile = (index: number) => {
    setSelectedFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) {
      alert("Please select a file or folder to upload.");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append("file", file);
    });
    const uploadToastId = toast.loading("File uploading...", {
      position: "top-right",
      autoClose: false,
      hideProgressBar: false,
      closeOnClick: false,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
    });

    try {
      setLoading(true);
      const token = await getIdToken();
      setIsDialogOpen(false);
      const response = await axiosPublic.post(
        "/api/v1/file_manager/upload_file",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
          onUploadProgress: (progressEvent) => {
            const percent = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 1)
            );
            setUploadProgress(percent);
          },
        }
      );
      console.log(response);
      if (response.status === 201) {
        toast.update(uploadToastId, {
          render: `File${selectedFiles.length > 1 ? "s" : ""} uploaded successfully!`,
          type: "success",
          isLoading: false,
          autoClose: 2000,
        });
        console.log("Upload successful:", response.data);
        if (Array.isArray(response.data)) {
          response.data.forEach((fileInfo) =>
            console.log(`Uploaded: ${fileInfo.file_name}, UID: ${fileInfo.uid}`)
          );
        } else {
          console.log(`Uploaded: ${response.data.file_name}, UID: ${response.data.uid}`);
        }
      } else {
        throw new Error(`Unexpected status code: ${response.status}`);
      }
    } catch (error) {
      console.error("Error uploading files:", error);
      toast.error("Failed to upload file", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
    } finally {
      setUploadProgress(0);
      setLoading(false);
      setSelectedFiles([]);
      refreshFiles();
    }
  };

  const handleChooseFile = () => {
    fileInputRef.current?.click();
  };

  useEffect(() => {
    if (!isDialogOpen) {
      setSelectedFiles([]);
      setUploadType("file");
    }
  }, [isDialogOpen]);

  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger asChild>
        <Button className="flex items-center">
          <Upload size={20} /> Upload
        </Button>
      </DialogTrigger>
      <DialogContent className="w-[400px] h-[400px]">
        <DialogHeader>
          <DialogTitle>Upload Files or Folders</DialogTitle>
        </DialogHeader>

        <div className="flex flex-col space-y-4">
          <Select
            onValueChange={(value: "file" | "folder") => setUploadType(value)}
            defaultValue="file"
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select upload type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="file">
                <div className="flex items-center gap-2">
                  <File size={16} /> File
                </div>
              </SelectItem>
              <SelectItem value="folder">
                <div className="flex items-center gap-2">
                  <Folder size={16} /> Folder
                </div>
              </SelectItem>
            </SelectContent>
          </Select>

          <div
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            className={`p-6 border-2 border-dashed rounded-lg ${
              isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300"
            }`}
          >
            <p className="text-center text-gray-600">
              Drag and drop your {uploadType === "file" ? "files " : "folder "}
              here, or click below to select.
            </p>
          </div>

          <input
            type="file"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileChange}
            multiple
            {...(uploadType === "folder"
              ? { webkitdirectory: "true", directory: "true" }
              : {})}
          />
          <Button
            variant="outline"
            className="w-full"
            onClick={handleChooseFile}
          >
            Choose {uploadType === "file" ? "Files" : "Folder"}
          </Button>

          {selectedFiles.length > 0 && (
            <div className="space-y-2 max-h-40 overflow-auto p-2 border border-gray-200 rounded-lg">
              {selectedFiles.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-2 border-b last:border-none"
                >
                  <div className="flex-1 min-w-0">
                    <span
                      className="block text-sm text-gray-700 truncate max-w-80"
                      title={file.name}
                    >
                      {file.name}
                    </span>
                  </div>
                  <button
                    onClick={() => handleRemoveFile(index)}
                    className="text-red-500 hover:text-red-700 flex-shrink-0"
                  >
                    <X size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}
          <Progress value={uploadProgress} />

          {!loading ? (
            <Button onClick={handleUpload} className="w-full">
              Upload
            </Button>
          ) : (
            <Button onClick={handleUpload} disabled className="w-full">
              Uploading
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default FileUpload;
