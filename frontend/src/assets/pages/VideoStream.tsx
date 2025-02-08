import { ArrowLeft } from "lucide-react";
import React from "react";
import ReactPlayer from "react-player";
import { useLocation, useNavigate } from "react-router-dom";

const VideoStreamPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { url } = location.state as { url: string };
  console.log(url);
  return (
    <div className="flex min-h-screen">
      <main className="flex-1 p-6 bg-gray-100">
        <button
            onClick={() => navigate(-1)}
            className="flex items-center space-x-2 mt-4 bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition duration-200"
          >
            <ArrowLeft className="w-5 h-5" />
          Go Back
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Play Video</h1>
        <div className="mt-6">
          <div className="player-wrapper">
            <ReactPlayer
              className="react-player"
              url={url}
              width="80%"
              height="80%"
              controls={true}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default VideoStreamPage;
