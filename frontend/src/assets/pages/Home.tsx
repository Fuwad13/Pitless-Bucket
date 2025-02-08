import React from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const Home: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="text-center space-y-6">
        <h1 className="text-5xl font-bold text-gray-900">
          Welcome to <span className="text-blue-600">Pitless Bucket</span>
        </h1>
        <p className="text-xl text-gray-600">
          Your private aggregate cloud storage platform.
        </p>
        <p className="text-lg text-gray-500">
          Store, view and dowload you files with ease!
        </p>
        <Button>
          <Link to="/signup">Try Pitless Bucket for Free</Link>
        </Button>
      </div>
    </div>
  );
};

export default Home;
