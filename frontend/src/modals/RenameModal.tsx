"use client";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import React, { useContext, useState } from "react";
import { toast } from "react-toastify";
import useAxiosPublic from "../hooks/AxiosPublic";
import { AuthContext } from "@/app/AuthContext";

interface RenameModalProps {
  file: {
    file_name: string;
    extension: string;
    uid: string;
  };
  isOpen: boolean;
  onClose: () => void;
  refreshFiles: () => void;
}

const RenameModal: React.FC<RenameModalProps> = ({
  file,
  isOpen,
  onClose,
  refreshFiles,
}) => {
  const [fileNameWithoutExtension, setFileNameWithoutExtension] = useState(
    file.file_name.split(".").slice(0, -1).join(".")
  );
  const [loading, setLoading] = useState(false);
  const axiosPublic = useAxiosPublic();
  const { getIdToken } = useContext(AuthContext)!;

  const handleRename = async () => {
    if (!fileNameWithoutExtension.trim()) {
      toast.error("Please enter a valid name", {
        position: "top-right",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
      return;
    }

    try {
      setLoading(true);
      const token = await getIdToken();
      const newFileName = `${fileNameWithoutExtension}.${file.extension}`;

      const response = await axiosPublic.put(
        `/api/v1/file_manager/rename_file`,
        null,
        {
          params: {
            file_id: file.uid,
            new_name: newFileName,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("response:", response);
      if (response.status !== 200) {
        throw new Error("Failed to rename file");
      }

      toast.success("File renamed successfully!", {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: false,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });

      onClose();
      refreshFiles();
    } catch (error) {
      console.error("Error renaming file:", error);
      toast.error("Failed to rename file", {
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
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="w-[600px]">
        <DialogHeader>
          <DialogTitle>Rename File</DialogTitle>
          <DialogDescription>Enter a new name for the file.</DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <Input
            value={fileNameWithoutExtension}
            onChange={(e) => setFileNameWithoutExtension(e.target.value)}
            placeholder="Enter new name"
          />
        </div>
        <DialogFooter>
          <Button onClick={handleRename} disabled={loading} className="w-full">
            {loading ? "Renaming..." : "Rename"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default RenameModal;
