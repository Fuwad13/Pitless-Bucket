import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Login from "./assets/pages/Login";
import Root from "./assets/routes/root";
import Home from "./assets/pages/Home";
import Dashboard from "./assets/pages/Dashboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    // element: <Login />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/dashboard",
        element: <Dashboard />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
