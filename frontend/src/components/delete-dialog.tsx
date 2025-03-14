"use client";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import useAxiosPublic from "@/hooks/use-axios";

interface DeleteDialogProps {
  fileId: string;
  children: React.ReactNode;
}

export const DeleteDialog = ({ fileId, children }: DeleteDialogProps) => {
  const router = useRouter();
  const axiosPublic = useAxiosPublic();
  const [isDeleting, setIsDeleting] = useState(false);

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>{children}</AlertDialogTrigger>
      <AlertDialogContent onClick={(e) => e.stopPropagation()}>
        <AlertDialogHeader>
          <AlertDialogTitle>
            Are you sure you want to delete this file?
          </AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={(e) => e.stopPropagation()}>
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            disabled={isDeleting}
            onClick={async (e) => {
              e.stopPropagation();
              setIsDeleting(true);
              try {
                await axiosPublic.delete("/api/v1/drive/delete_file", {
                  params: { file_id: fileId },
                });
                toast.success("File deleted successfully");
                router.push("/dashboard");
              } catch (error) {
                console.error("Delete error:", error);
                toast.error("Something went wrong");
              } finally {
                setIsDeleting(false);
              }
            }}
            className="btn-danger"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};
