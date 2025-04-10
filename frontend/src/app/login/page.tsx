"use client";
import { useEffect, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EyeIcon, EyeOffIcon } from "lucide-react";
import { toast } from "react-toastify";
import { FaGoogle } from "react-icons/fa";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  auth,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
} from "../firebase.js";
import { onAuthStateChanged } from "firebase/auth";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        router.push("/dashboard");
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleEmailLogin = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      toast.success("Login Successful!");
      router.push("/dashboard");
    } catch (error) {
      toast.error("Invalid email or password.");
      setError("Invalid email or password.");
      console.log(error);
    }
  };

  const handleGoogleLogin = async () => {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
      toast.success("Login Successful!");
      router.push("/dashboard");
    } catch (error) {
      toast.error("Google login failed.");
      console.log(error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center text-gray-900">
          Login to <span className="text-blue-600">Pitless Bucket</span>
        </h1>
        <form onSubmit={handleEmailLogin} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 flex items-center pr-3"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOffIcon className="h-5 w-5 text-gray-500" />
                ) : (
                  <EyeIcon className="h-5 w-5 text-gray-500" />
                )}
              </button>
            </div>
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" className="w-full">
            Login
          </Button>
        </form>
        <div className="flex items-center justify-center space-x-2">
          <hr className="flex-1 border-t border-gray-300" />
          <span className="text-gray-600">OR</span>
          <hr className="flex-1 border-t border-gray-300" />
        </div>
        <div className="mt-4">
          <Button
            type="button"
            onClick={handleGoogleLogin}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white flex items-center justify-center"
          >
            <FaGoogle />
            <span className="mr-2">Login with Google</span>
          </Button>
        </div>
        <p className="text-center text-sm text-gray-400">
          Don&apos;t Have an Account?{" "}
          <Link className="text-blue-500" href="/signup">
            Create one
          </Link>{" "}
          now!
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
