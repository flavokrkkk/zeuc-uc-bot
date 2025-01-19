import { useRewards } from "@/features/scores/hooks/useRewards";
// import { useUser } from "@/features/user/hooks/useUser";
import { Suspense } from "react";
import { Outlet } from "react-router-dom";

const MainPage = () => {
  // useUser();
  useRewards();
  return (
    <Suspense fallback={<div className="h-screen w-full">Loading..</div>}>
      <Outlet />
    </Suspense>
  );
};

export default MainPage;
