import React from 'react';
import ReactPlayer from 'react-player';
import { useLocation } from 'react-router-dom';


const VideoStreamPage : React.FC = () => {
    const location = useLocation();
    const { url } = location.state as { url: string };
    console.log(url);
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
              url={url}
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

export default VideoStreamPage;
