import { Outlet } from "react-router-dom";
import Navbar from "../customComponents/Navbar";

const root = () => {
  return (
    <div>
      <Navbar />
      <Outlet />
    </div>
  );
};

export default root;
