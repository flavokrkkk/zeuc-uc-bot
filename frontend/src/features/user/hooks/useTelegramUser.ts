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
      const mockUser = { id: 1, username: "test_1" };
      if (mockUser) {
        Promise.all([setUserCredentials(mockUser)]).then(([payload]) => {
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
