import { Suspense } from "react";
import { Outlet } from "react-router-dom";

const RootPage = () => {
  return (
    <div className="bg-purple-400 h-screen w-screen p-3">
      <Suspense fallback={<h1>Loading...</h1>}>
        <Outlet />
      </Suspense>
    </div>
  );
};

export default RootPage;
