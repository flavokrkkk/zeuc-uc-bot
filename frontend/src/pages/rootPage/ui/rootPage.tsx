import { useTelegramUser } from "@/features/user/hooks/useTelegramUser";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { Suspense } from "react";
import { Outlet } from "react-router-dom";

const RootPage = () => {
  useTelegramUser();
  return (
    <div className="bg-dark-100 h-screen w-screen p-3">
      <Suspense fallback={<h1>Loading...</h1>}>
        <Icon
          type={IconTypes.BG_OUTLINED}
          className="absolute top-0 right-0 w-full h-full max-w-[100vw] max-h-[100vh] overflow-hidden pointer-events-none"
        />
        <Outlet />
        <Icon
          type={IconTypes.BG_UC_OUTLINED}
          className="fixed bottom-28 rotate-12 left-4 overflow-hidden z-10 filter blur-sm"
        />
      </Suspense>
    </div>
  );
};

export default RootPage;
