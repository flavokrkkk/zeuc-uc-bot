import { useTelegramUser } from "@/features/user/hooks/useTelegramUser";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { Suspense } from "react";
import { Outlet } from "react-router-dom";

const RootPage = () => {
  useTelegramUser();
  return (
    <div className="bg-dark-100 h-screen w-screen p-3 relative">
      <Suspense fallback={<h1>Loading...</h1>}>
        {/* Фоновые иконки */}
        <div className="absolute inset-0 z-0">
          <Icon
            type={IconTypes.BG_OUTLINED}
            className="w-full h-full max-w-[100vw] max-h-[100vh] overflow-hidden pointer-events-none"
          />
          <Icon
            type={IconTypes.BG_UC_OUTLINED}
            className="fixed bottom-28 rotate-12 left-4 overflow-hidden filter blur-sm pointer-events-none"
          />
        </div>

        {/* Основной контент */}
        <div className="relative z-10">
          <Outlet />
        </div>
      </Suspense>
    </div>
  );
};

export default RootPage;
