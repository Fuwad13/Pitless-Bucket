import VideoPlayer from "./videoPlayer";

interface WatchVideoPageProps {
  params: Promise<{ videoFileId: string }>;
}

const WatchVideoPage = async ({ params }: WatchVideoPageProps) => {
  const { videoFileId } = await params;
  const videoUrl = `http://localhost:8000/api/v1/drive/video-stream?file_id=${videoFileId}`;
  return <VideoPlayer videoUrl={videoUrl} />;
};

export default WatchVideoPage;
