import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Login from "./assets/pages/Login";
import Root from "./assets/routes/root";

const router = createBrowserRouter([
  {
    path: "/",
    // element: <Root />,
    element: <Login />,
    children: [
      {
        path: "/login",
        element: <Login />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
