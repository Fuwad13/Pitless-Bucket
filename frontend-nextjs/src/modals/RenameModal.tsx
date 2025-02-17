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
  const [newName, setNewName] = useState(file.file_name);
  const [loading, setLoading] = useState(false);
  const axiosPublic = useAxiosPublic();
  const { getIdToken } = useContext(AuthContext);

  const handleRename = async () => {
    if (!newName.trim()) {
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
      console.log("newName:", typeof newName);
      console.log("file.uid:", typeof file.uid);

      setLoading(true);
      const token = await getIdToken();
      const response = await axiosPublic.put(
        `/api/v1/file_manager/rename_file`,
        null,
        {
          params: {
            file_id: file.uid,
            new_name: newName,
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
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
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
