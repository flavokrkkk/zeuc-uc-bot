import { useActions } from "@/shared/hooks/useActions";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const useTelegramUser = () => {
  const { setUserCredentials } = useActions();
  const navigate = useNavigate();

  useEffect(() => {
    if (window.Telegram) {
      const user = window.Telegram.WebApp.initDataUnsafe?.user;
      // const user = { id: 1, username: "test_1" };
      if (user) {
        Promise.all([setUserCredentials(user)]).then(([payload]) => {
          const { meta }: { meta: { requestStatus: string } } =
            payload as unknown as {
              meta: { requestStatus: "rejected" | "fulfilled" };
            };
          if (meta.requestStatus === "fulfilled") {
            navigate(ERouteNames.CATALOG_PAGE);
            return;
          }
          if (meta.requestStatus === "rejected") {
            navigate(ERouteNames.AUTH_ERROR);
            return;
          }
        });
      }
    }
  }, []);
};
