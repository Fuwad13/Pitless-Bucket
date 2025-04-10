"use client";
import ReactPlayer from "react-player";
import { useContext } from "react";
import { AuthContext } from "@/app/AuthContext";
import UnauthorizedPage from "@/components/customComponents/unauthorisedPage";

interface VideoPlayerProps {
  videoUrl: string;
}

const VideoPlayer = ({ videoUrl }: VideoPlayerProps) => {
  const { currentUser } = useContext(AuthContext)!;
  if (!currentUser) {
    return <UnauthorizedPage />;
  }
  // TODO : check if user has access to the video
  return (
    <div className="flex min-h-screen">
      <aside className="hidden md:flex flex-col w-64 bg-blue-50 p-6 space-y-4 shadow-lg">
        <h2 className="text-2xl font-bold text-blue-600">Pitless Bucket</h2>
      </aside>
      <main className="flex-1 p-6 bg-gray-100">
        <h1 className="text-3xl font-bold text-gray-900">Play Video</h1>
        <div className="mt-6">
          <div className="player-wrapper">
            <ReactPlayer
              className="react-player"
              url={videoUrl}
              width="100%"
              height="100%"
              controls={true}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default VideoPlayer;
