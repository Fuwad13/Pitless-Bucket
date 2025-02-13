"use client";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  MoreVertical,
  Trash2,
  ImageIcon,
  PlayIcon,
  DownloadIcon,
  FolderPen,
} from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";
import FileExtensioIcon from "@/misc/FileExtensioIcon";
import RenameModal from "@/modals/RenameModal";

interface FileCardProps {
  file: {
    uid: string;
    user_id: string;
    file_name: string;
    content_type: string;
    extension: string;
    size: number;
    created_at: Date;
    updated_at: Date;
  };
  onDownload: (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => Promise<void>;
  onDelete: (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => Promise<void>;
  refreshFiles: () => void;
}

const FileCard: React.FC<FileCardProps> = ({
  file,
  onDownload,
  onDelete,
  refreshFiles,
}) => {
  const allowedVideoExtensions = ["mp4", "webm", "mkv"];
  const allowedImageExtensions = ["png", "jpg", "jpeg"];
  const router = useRouter();
  const [isDownloading, setIsDownloading] = useState(false);
  const [isRenameModalOpen, setIsRenameModalOpen] = useState(false);

  const fileNameWithoutExtension = file.file_name.includes(".")
    ? file.file_name.substring(0, file.file_name.lastIndexOf("."))
    : file.file_name;

  const handleDownload = async (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => {
    setIsDownloading(true);
    try {
      await onDownload(file);
    } catch (error) {
      console.error("Download error:", error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleDelete = async (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => {
    try {
      await onDelete(file);
    } catch (error) {
      console.error("Delete error:", error);
    }
  };

  const formatFileSize = (size: number): string => {
    if (size === 0) return "0 Bytes";

    const units = ["Bytes", "KB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(size) / Math.log(1024));
    const formattedSize = (size / Math.pow(1024, i)).toFixed(2);

    return `${formattedSize} ${units[i]}`;
  };

  return (
    <Card className="hover:shadow-lg transition-transform transform relative border border-gray-200">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          {FileExtensioIcon(file.extension)}
          <span
            className="truncate min-h-8 overflow-hidden text-ellipsis whitespace-nowrap block max-w-[220px] md:max-w-[300px] lg:max-w-[400px]"
            title={file.file_name}
          >
            {fileNameWithoutExtension}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <p className="text-gray-500 text-sm font-medium">{file.extension}</p>
          <p className="text-gray-500 text-sm font-medium">
            {formatFileSize(file.size)}
          </p>
        </div>
      </CardContent>

      {/* Dropdown Menu */}
      <DropdownMenu.Root>
        <DropdownMenu.Trigger asChild>
          <button
            className="absolute top-2 right-2 p-1 rounded-full border hover:bg-gray-100 transition"
            aria-label="More options"
          >
            <MoreVertical className="w-5 h-5 text-gray-600" />
          </button>
        </DropdownMenu.Trigger>

        <DropdownMenu.Portal>
          <DropdownMenu.Content className="min-w-[140px] bg-white border border-gray-200 rounded-md shadow-lg z-50">
            {allowedVideoExtensions.includes(file.extension) && (
              <DropdownMenu.Item
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                onClick={() => router.push(`/watch/${file.uid}`)}
              >
                <PlayIcon size={16} className="text-gray-500" /> Play Video
              </DropdownMenu.Item>
            )}
            {allowedImageExtensions.includes(file.extension) && (
              <DropdownMenu.Item
                className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                // TODO: Implement image preview
                onClick={() => router.push(`/image-preview/${file.uid}`)}
              >
                <ImageIcon size={16} className="text-gray-500" /> View Image
              </DropdownMenu.Item>
            )}
            <DropdownMenu.Item
              className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleDownload(file)}
              disabled={isDownloading}
            >
              <DownloadIcon size={16} className="text-gray-500" /> Download
            </DropdownMenu.Item>
            <DropdownMenu.Item
              className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
              onClick={() => setIsRenameModalOpen(true)}
            >
              <FolderPen size={16} className="text-gray-500" /> Rename
            </DropdownMenu.Item>
            <DropdownMenu.Item
              className="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleDelete(file)}
            >
              <Trash2 size={16} className="text-red-500" /> Delete
            </DropdownMenu.Item>
          </DropdownMenu.Content>
        </DropdownMenu.Portal>
      </DropdownMenu.Root>

      {/* Rename Modal */}
      <RenameModal
        file={file}
        isOpen={isRenameModalOpen}
        onClose={() => setIsRenameModalOpen(false)}
        refreshFiles={refreshFiles}
      />

      {/* Downloading Progress Bar */}
      {isDownloading && (
        <div className="absolute bottom-2 right-2 p-2 bg-gray-200 rounded-full flex items-center justify-center">
          Downloading
        </div>
      )}
    </Card>
  );
};

export default FileCard;
