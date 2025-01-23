import { ViewerContext } from "@/entities/viewer/models/context/providers";
import { useAsyncPacks } from "@/features/packs/hooks/useAsyncPacks";
import { useRewards } from "@/features/scores/hooks/useRewards";
import { useUser } from "@/features/user/hooks/useUser";
import { Suspense, useContext } from "react";
import { Outlet } from "react-router-dom";

const MainPage = () => {
  const { isAuthenticated } = useContext(ViewerContext);
  useUser(isAuthenticated);
  useRewards(isAuthenticated);
  useAsyncPacks(isAuthenticated);
  return (
    <Suspense fallback={<div className="h-screen w-full">Loading..</div>}>
      <Outlet />
    </Suspense>
  );
};

export default MainPage;
