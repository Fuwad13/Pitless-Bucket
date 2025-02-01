import React from "react";
import { Link } from "react-router-dom";
import FileUpload from "../modals/FileUpload";
import { Folder, File, Settings, Home, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// dummy data to see if the card style works remove it later when we add the backend data fetch
const filesAndFolders = [
  { id: 1, name: "Project Files", type: "folder" },
  { id: 2, name: "Resume.pdf", type: "file" },
  { id: 3, name: "Design Assets", type: "folder" },
  { id: 4, name: "Meeting Notes.docx", type: "file" },
];

const Dashboard: React.FC = () => {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar for Large Screens, we see this at desktop*/}
      <aside className="hidden md:flex flex-col w-64 bg-blue-50 p-6 space-y-4 shadow-lg">
        <h2 className="text-2xl font-bold text-blue-600">Pitless Bucket</h2>
        <nav className="space-y-3">
          <FileUpload />
          <Link
            to="/"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Home size={20} /> Home
          </Link>

          <Link
            to="/settings"
            className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
          >
            <Settings size={20} /> Settings
          </Link>
        </nav>
      </aside>

      {/* Mobile Sidebar (Drawer) needs come position fixing for drop down icon, can just move it to navbar later*/}
      <Sheet>
        <SheetTrigger asChild>
          <Button className="md:hidden absolute top-4 left-4">
            <Menu />
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
          <nav className="space-y-4">
            <FileUpload />
            <Link
              to="/"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Home size={20} /> Home
            </Link>

            <Link
              to="/settings"
              className="flex items-center gap-3 text-gray-700 hover:text-blue-600"
            >
              <Settings size={20} /> Settings
            </Link>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Main Content section */}
      <main className="flex-1 p-6 bg-gray-100">
        <h1 className="text-3xl font-bold text-gray-900">
          Your Files & Folders
        </h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          {filesAndFolders.map((item) => (
            <Card key={item.id} className="hover:shadow-md transition">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {item.type === "folder" ? (
                    <Folder className="text-blue-500" />
                  ) : (
                    <File className="text-gray-500" />
                  )}
                  {item.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 text-sm">
                  {item.type === "folder" ? "Folder" : "File"}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
