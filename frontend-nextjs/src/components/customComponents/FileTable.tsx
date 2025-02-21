"use client";
import React from "react";
import { Download, Trash2, Edit } from "lucide-react";
import FileExtensioIcon from "@/misc/FileExtensioIcon";

interface FileType {
  uid: string;
  file_name: string;
  content_type: string;
  extension: string;
  size: number;
  created_at: Date;
}

interface FileTableProps {
  files: FileType[];
  onDownload: (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => void;
  onDelete: (file: {
    file_name: string;
    extension: string;
    uid: string;
  }) => void;
  onEdit: (file: { file_name: string; extension: string; uid: string }) => void;
}

const FileTable: React.FC<FileTableProps> = ({
  files,
  onDownload,
  onDelete,
  onEdit,
}) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="py-3 px-4 text-left text-sm font-medium text-gray-600 whitespace-nowrap">
              File Name
            </th>
            <th className="py-3 px-4 text-left text-sm font-medium text-gray-600 whitespace-nowrap">
              Type
            </th>
            <th className="py-3 px-4 text-left text-sm font-medium text-gray-600 whitespace-nowrap">
              Size
            </th>
            <th className="py-3 px-4 text-left text-sm font-medium text-gray-600 whitespace-nowrap">
              Created At
            </th>
            <th className="py-3 px-4 text-left text-sm font-medium text-gray-600 whitespace-nowrap">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {files.map((file) => (
            <tr key={file.uid} className="hover:bg-gray-50">
              <td className="py-3 px-4 text-sm text-gray-800 flex gap-2">
                {FileExtensioIcon(file.extension)}
                {file.file_name}
              </td>

              <td className="py-3 px-4 text-sm text-gray-800">
                {file.content_type}
              </td>

              <td className="py-3 px-4 text-sm text-gray-800">
                {(file.size / 1024).toFixed(2)} KB
              </td>

              <td className="py-3 px-4 text-sm text-gray-800">
                {new Date(file.created_at).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "short",
                  day: "numeric",
                })}
              </td>

              <td className="py-3 px-4 text-sm text-gray-800 space-x-2">
                <button
                  onClick={() =>
                    onDownload({
                      file_name: file.file_name,
                      extension: file.extension,
                      uid: file.uid,
                    })
                  }
                  className="text-blue-600 hover:text-blue-800"
                  title="Download"
                >
                  <Download size={16} />
                </button>

                <button
                  onClick={() =>
                    onEdit({
                      file_name: file.file_name,
                      extension: file.extension,
                      uid: file.uid,
                    })
                  }
                  className="text-green-600 hover:text-green-800"
                  title="Edit"
                >
                  <Edit size={16} />
                </button>

                <button
                  onClick={() =>
                    onDelete({
                      file_name: file.file_name,
                      extension: file.extension,
                      uid: file.uid,
                    })
                  }
                  className="text-red-600 hover:text-red-800"
                  title="Delete"
                >
                  <Trash2 size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FileTable;
