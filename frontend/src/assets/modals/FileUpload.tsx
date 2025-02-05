import React, { useState, useCallback, useRef, useEffect } from "react";
import { Upload, Folder, File, X } from "lucide-react";
import { Button } from "@/components/ui/button";
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

interface FileUploadProps {
  refreshFiles: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ refreshFiles }) => {
  const [uploadType, setUploadType] = useState<"file" | "folder">("file");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const axiosPublic = useAxiosPublic();

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

    try {
      setLoading(true);
      const response = await axiosPublic.post("/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (!response) {
        throw new Error("Upload failed");
      }

      console.log("Upload successful:", response.data);
      toast.success("File uploaded successfully!", {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
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
      <DialogContent className="sm:max-w-md max-w-[90vw]">
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
