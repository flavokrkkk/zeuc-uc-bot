import { ViewerContext } from "@/entities/viewer/models/context/providers";
import Menu from "@/features/menu/ui/menu";
import { useTelegramUser } from "@/features/user/hooks/useTelegramUser";
import { pathNavigate } from "@/shared/libs/utils/pathNavigate";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import clsx from "clsx";
import { Suspense, useContext } from "react";
import { Outlet, useLocation } from "react-router-dom";

const RootPage = () => {
  const pathName = useLocation();
  const { isAuthenticated } = useContext(ViewerContext);
  useTelegramUser();
  return (
    <div className="bg-dark-100 h-[96vh] w-screen p-3 relative flex flex-col justify-between">
      <div className="absolute inset-0 bg-black opacity-30 z-0" />{" "}
      <Suspense fallback={<h1>Loading...</h1>}>
        <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
          <Icon
            type={IconTypes.BG_OUTLINED}
            className="w-full h-full max-w-[100vw] max-h-[100vh]"
          />
          <Icon
            type={IconTypes.BG_UC_OUTLINED}
            className="absolute bottom-28 left-4 rotate-12 filter blur-sm bg-black opacity-10"
          />
        </div>
        <div
          className={clsx(
            "relative z-10 flex-1 ",
            pathName.pathname === ERouteNames.PAYMENT_PAGE
              ? "overflow-auto "
              : "overflow-hidden "
          )}
        >
          <Outlet />
        </div>
      </Suspense>
      {isAuthenticated && (
        <div className="text-white flex flex-col items-center bg-gray-dark-200 relative p-4 px-9 rounded-xl">
          <Menu navigates={pathNavigate} />
          <span className="absolute -bottom-0 w-[239px] rounded-2xl" />
        </div>
      )}
    </div>
  );
};

export default RootPage;
