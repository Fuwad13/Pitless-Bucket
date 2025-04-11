"use client";
import axios from "axios";
const axiosPublic = axios.create({
  baseURL: "https://promoted-cardinal-handy.ngrok-free.app",
  headers: {
    "ngrok-skip-browser-warning": "69696",
  },
});
const useAxiosPublic = () => {
  return axiosPublic;
};

export default useAxiosPublic;
