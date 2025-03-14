"use client";
import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { ArrowLeft, Loader2 } from "lucide-react";

const ImagePreview: React.FC = () => {
  const location = useLocation();
  const { url } = location.state || {};
  const navigate = useNavigate();

  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!url) {
      setError("No URL provided.");
      setLoading(false);
      return;
    }

    const fetchImagePreview = async () => {
      try {
        const response = await axios.get(url, {
          responseType: "blob",
        });

        const imageBlobUrl = URL.createObjectURL(response.data);
        setImageSrc(imageBlobUrl);
      } catch (err) {
        setError("Failed to load image preview.");
        console.log(err);
      } finally {
        setLoading(false);
      }
    };

    fetchImagePreview();
  }, [url]);
  const handleGoBack = () => {
    navigate(-1);
  };

  if (loading)
    return (
      <div className="min-h-screen flex justify-center items-center col-span-3">
        <div className="flex flex-col-reverse items-center justify-center gap-2">
          <p>Loading Image</p>
          <Loader2 className="w-6 h-6 animate-spin text-gray-500" />
        </div>
      </div>
    );
  if (error) return <div>{error}</div>;

  return (
    <div className="w-11/12 mx-auto">
      <button
        onClick={handleGoBack}
        className="flex items-center space-x-2 mt-4 bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition duration-200"
      >
        <ArrowLeft className="w-5 h-5" />
        Go Back
      </button>
      <h1 className="text-3xl font-bold text-gray-900 py-2">Image Preview</h1>
      <div className="flex flex-col justify-center items-center h-full border mb-10 rounded-xl p-8">
        <div>{imageSrc && <img src={imageSrc} alt="Image Preview" />}</div>
      </div>
    </div>
  );
};

export default ImagePreview;
