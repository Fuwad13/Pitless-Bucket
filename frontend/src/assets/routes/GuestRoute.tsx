import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../auth/AuthContext";

interface GuestRouteProps {
  children: React.ReactNode;
}

const GuestRoute: React.FC<GuestRouteProps> = ({ children }) => {
  const { currentUser } = useContext(AuthContext);

  return !currentUser ? children : <Navigate to="/dashboard" />;
};

export default GuestRoute;
