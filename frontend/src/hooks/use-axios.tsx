import axios from "axios";
const axiosPublic = axios.create({
  // baseURL: "https://promoted-cardinal-handy.ngrok-free.app", Uncomment this line to use ngrok
  // baseURL: "https://pitless-bucket.onrender.com", // Comment this line to use ngrok
  baseURL: "http://127.0.0.1:8000", // Comment this line to use ngrok
  headers: {
    "ngrok-skip-browser-warning": "69696",
  },
});
const useAxiosPublic = () => {
  return axiosPublic;
};

export default useAxiosPublic;
