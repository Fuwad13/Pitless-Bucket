import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import { ToastContainer } from "react-toastify";
import Login from "./assets/pages/Login";
import Signup from "./assets/pages/SignUp";
import Root from "./assets/routes/root";
import Home from "./assets/pages/Home";
import Dashboard from "./assets/pages/Dashboard";
import VideoStream from "./assets/pages/VideoStream";
import { AuthProvider } from "./auth/AuthContext";
import PrivateRoute from "./assets/routes/PrivateRoute";
import GuestRoute from "./assets/routes/GuestRoute";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/",
        element: (
          <GuestRoute>
            <Home />
          </GuestRoute>
        ),
      },
      {
        path: "/login",
        element: (
          <GuestRoute>
            <Login />
          </GuestRoute>
        ),
      },
      {
        path: "/signup",
        element: (
          <GuestRoute>
            <Signup />
          </GuestRoute>
        ),
      },
      {
        path: "/dashboard",
        element: (
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        ),
      },
      {
        path: "/video-stream",
        element: <VideoStream />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
      <ToastContainer position="top-right" />
    </AuthProvider>
  </StrictMode>
);
