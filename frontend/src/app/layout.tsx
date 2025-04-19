import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "./AuthContext";
import Navbar from "@/components/customComponents/Navbar";
import ToastProvider from "@/components/customComponents/toastProvider";
import Chatbot from "@/components/customComponents/Chatbot";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Pitless Bucket",
  description: "Your private aggregated cloud storage platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <Navbar />
          <ToastProvider>{children}</ToastProvider>
          <Chatbot />
        </AuthProvider>
      </body>
    </html>
  );
}
