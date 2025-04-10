import axios from "axios";
const axiosPublic = axios.create({
  baseURL: "https://promoted-cardinal-handy.ngrok-free.app",
});
const useAxiosPublic = () => {
  return axiosPublic;
};

export default useAxiosPublic;
