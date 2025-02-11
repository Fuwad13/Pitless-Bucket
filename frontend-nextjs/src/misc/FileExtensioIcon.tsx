import {
  Folder,
  File,
  FileImage,
  FileText,
  FileSpreadsheet,
  FileArchive,
  FileCode,
  FileBadge,
  FileAudio,
  FileVideo,
  FileScan,
} from "lucide-react";

const FileExtensioIcon = (type: string) => {
  if (type === "folder") return <Folder className="text-blue-500" size={20} />;

  const extension = type.toLowerCase();

  switch (extension) {
    case "png":
    case "jpg":
    case "jpeg":
    case "gif":
    case "webp":
      return <FileImage className="text-yellow-500" size={20} />;

    case "txt":
    case "md":
      return <FileText className="text-gray-500" size={20} />;

    case "csv":
    case "xls":
    case "xlsx":
      return <FileSpreadsheet className="text-green-500" size={20} />;

    case "pdf":
      return <FileBadge className="text-red-500" size={20} />;

    case "zip":
    case "rar":
    case "7z":
      return <FileArchive className="text-orange-500" size={20} />;

    case "mp3":
    case "wav":
    case "ogg":
      return <FileAudio className="text-purple-500" size={20} />;

    case "mp4":
    case "avi":
    case "mov":
    case "mkv":
      return <FileVideo className="text-indigo-500" size={20} />;

    case "js":
    case "ts":
    case "jsx":
    case "tsx":
    case "py":
    case "java":
    case "cpp":
    case "c":
    case "html":
    case "css":
      return <FileCode className="text-blue-400" size={20} />;

    case "json":
    case "xml":
    case "yaml":
      return <FileScan className="text-teal-500" size={20} />;

    default:
      return <File className="text-gray-500" size={20} />;
  }
};

export default FileExtensioIcon;
