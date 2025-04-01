import { ViewerContext } from "@/entities/viewer/models/context/providers";
import { useAsyncPacks } from "@/features/packs/hooks/useAsyncPacks";
import { useRewards } from "@/features/scores/hooks/useRewards";
import { useUser } from "@/features/user/hooks/useUser";
import { useWebSocketEvents } from "@/shared/hooks/useSocketEvents";

import { Suspense, useContext } from "react";
import { Outlet } from "react-router-dom";
import { toast } from "sonner";

const MainPage = () => {
  const { isAuthenticated } = useContext(ViewerContext);

  useUser(isAuthenticated);
  useRewards(isAuthenticated);
  useAsyncPacks(isAuthenticated);

  useWebSocketEvents(
    "purchase_status",
    (data: {
      detail: "Оплата прошла успешно, но возможно не все коды активировались";
      event: string;
    }) => {
      toast.info(data.detail, {
        position: "top-center",
        duration: 30000,
        dismissible: true,
      });
    }
  );

  return (
    <Suspense fallback={<div className="h-screen w-full">Loading..</div>}>
      <Outlet />
    </Suspense>
  );
};

export default MainPage;
