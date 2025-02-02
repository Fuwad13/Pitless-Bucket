import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MoreVertical, Download, Trash2 } from "lucide-react";
import FileIcon from "../misc/FileIcon";
import { useState, useEffect } from "react";

interface FileCardProps {
  file: {
    name: string;
    type: string;
  };
  onDownload: (file: { name: string; type: string }) => Promise<void>;
}

const FileCard: React.FC<FileCardProps> = ({ file, onDownload }) => {
  const [isDownloading, setIsDownloading] = useState(false);

  const fileNameWithoutExtension = file.name.includes(".")
    ? file.name.substring(0, file.name.lastIndexOf("."))
    : file.name;

  const handleDownload = async (file: { name: string; type: string }) => {
    setIsDownloading(true);
    try {
      await onDownload(file);
    } catch (error) {
      console.error("Download error:", error);
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <Card className="hover:shadow-lg transition-transform transform relative border border-gray-200">
      <CardHeader>
        <CardTitle className="flex items-center gap-3">
          {FileIcon(file.type)}
          <span
            className="truncate min-h-8 overflow-hidden text-ellipsis whitespace-nowrap block max-w-[220px] md:max-w-[300px] lg:max-w-[400px]"
            title={file.name}
          >
            {fileNameWithoutExtension}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-500 text-sm font-medium">{file.type}</p>
      </CardContent>

      {/* Dropdown Menu */}
      <DropdownMenu.Root>
        <DropdownMenu.Trigger asChild>
          <button
            className="absolute top-2 right-2 p-1 rounded-full hover:bg-gray-100 transition"
            aria-label="More options"
          >
            <MoreVertical className="w-5 h-5 text-gray-600" />
          </button>
        </DropdownMenu.Trigger>

        <DropdownMenu.Portal>
          <DropdownMenu.Content className="min-w-[140px] bg-white border border-gray-200 rounded-md shadow-lg z-50">
            <DropdownMenu.Item
              className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleDownload(file)}
              disabled={isDownloading}
            >
              {isDownloading ? (
                <Download size={16} className="text-gray-500" />
              ) : (
                <Download size={16} className="text-gray-500" />
              )}
              {isDownloading ? "Downloading..." : "Download"}
            </DropdownMenu.Item>
            <DropdownMenu.Item
              className="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-gray-100 cursor-pointer"
              // onClick={() => handleDelete(file.id)}
            >
              <Trash2 size={16} className="text-red-500" /> Delete
            </DropdownMenu.Item>
          </DropdownMenu.Content>
        </DropdownMenu.Portal>
      </DropdownMenu.Root>

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
