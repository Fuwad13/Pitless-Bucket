import { useRouter } from "next/navigation";

const UnauthorizedPage = () => {
  const router = useRouter();
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Unauthorized</h1>
        <p className="text-gray-700">
          You are not authorised to view this page
        </p>
        <button
          onClick={() => router.push("/")}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
        >
          Homepage
        </button>
      </div>
    </div>
  );
};

export default UnauthorizedPage;
