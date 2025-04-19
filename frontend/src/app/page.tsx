"use client";
import React, { useContext, useEffect } from "react";
import { Button } from "@/components/ui/button"; // Assuming this path is correct
import Link from "next/link";
import { AuthContext } from "./AuthContext"; // Assuming this path is correct
import { Cloud, Link2, Combine, DownloadCloud, Sparkles } from "lucide-react";

// Reusable Feature Card component for cleaner structure
interface FeatureCardProps {
  icon: React.ElementType;
  title: string;
  description: string;
  iconColor?: string; // Optional color class for the icon
}

const FeatureCard: React.FC<FeatureCardProps> = ({
  icon: Icon,
  title,
  description,
  iconColor = "text-blue-500",
}) => (
  <div className="p-6 bg-white rounded-xl shadow-md border border-gray-100 flex flex-col items-center text-center transition-transform hover:scale-[1.03] duration-300">
    <Icon className={`h-10 w-10 ${iconColor} mb-4`} />
    <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
    <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
  </div>
);

const Home: React.FC = () => {
  const authContext = useContext(AuthContext);
  const currentUser = authContext?.currentUser;

  useEffect(() => {
    if (currentUser) {
      // Use Next.js router for client-side navigation if available and preferred
      // import { useRouter } from 'next/navigation';
      // const router = useRouter();
      // router.push('/dashboard');
      // Or keep window.location if simpler for this initial redirect
      window.location.href = "/dashboard";
    }
  }, [currentUser]);

  // Display loading indicator only if redirecting
  if (currentUser) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        <p className="text-gray-600 animate-pulse">
          Redirecting to dashboard...
        </p>
        {/* Optional: Add a spinner */}
      </div>
    );
  }

  // Render the landing page content
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 font-sans">
      {" "}
      {/* Added font-sans for baseline */}
      <main className="flex flex-1 flex-col items-center justify-center p-6 md:p-10 text-center">
        <div className="max-w-4xl mx-auto w-full">
          {/* Hero Section */}
          <section className="mb-14">
            <Cloud className="inline-block h-12 w-12 text-blue-500 mb-4 animate-bounce" />{" "}
            {/* Changed animation slightly */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
              Welcome to Pitless Bucket
            </h1>
            <p className="text-lg md:text-xl text-gray-700 max-w-2xl mx-auto mb-8 leading-relaxed">
              Tired of scattered files? Connect Google Drive, Dropbox, and more
              into{" "}
              <strong className="font-semibold text-blue-600">
                one simple, unified dashboard
              </strong>
              .
            </p>
            {/* <Button size="lg" asChild>
              <Link href="/signup">Get Started for Free</Link>
            </Button>
            <p className="mt-3 text-[12px] text-gray-500">
              Already Have an Account?{" "}
              <Link className="text-blue-600" href="/login">
                Login
              </Link>
            </p>
            <p className="mt-3 text-sm text-gray-500">
              Connect your accounts securely in minutes.
            </p> */}
          </section>

          {/* Features Section */}
          <section className="mb-20 w-full">
            <h2 className="text-3xl md:text-4xl font-semibold text-gray-800 mb-12 flex items-center justify-center gap-3">
              <Sparkles className="h-8 w-8 text-yellow-500" />
              Simplify Your Cloud Chaos
              <Sparkles className="h-8 w-8 text-yellow-500" />
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
              <FeatureCard
                icon={Link2}
                title="Connect All Accounts"
                description="Securely link multiple Google Drive & Dropbox accounts. More coming soon!"
                iconColor="text-green-500"
              />
              <FeatureCard
                icon={Combine}
                title="Unified File View"
                description="See files from all connected clouds together. Stop searching, start finding!"
                iconColor="text-purple-500"
              />
              <FeatureCard
                icon={DownloadCloud}
                title="Easy Access & Download"
                description="Grab any file you need directly through Pitless Bucket, no matter where it lives."
                iconColor="text-cyan-500"
              />
            </div>
            <div className="mt-10">
              <Button size="lg" asChild>
                <Link href="/signup">Get Started for Free</Link>
              </Button>
              <p className="mt-3 text-[12px] text-gray-500">
                Already Have an Account?{" "}
                <Link className="text-blue-600" href="/login">
                  Login
                </Link>
              </p>
              <p className="mt-3 text-sm text-gray-500">
                Connect your accounts securely in minutes.
              </p>
            </div>
          </section>

          {/* Final Info / Learn More */}
          <section className="">
            <p className="text-lg md:text-xl text-gray-700 mb-4">
              Ready to experience a calmer cloud?
            </p>
            <Link
              href="/about"
              className="text-base text-blue-600 hover:text-blue-800 hover:underline transition-colors"
            >
              Learn more about how Pitless Bucket
            </Link>
          </section>
        </div>
      </main>
      {/* Footer */}
      <footer className="p-6 text-center text-xs text-gray-500 border-t border-gray-200/60 mt-12">
        {" "}
        {/* Added subtle top border */}© {new Date().getFullYear()} Pitless
        Bucket. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;
