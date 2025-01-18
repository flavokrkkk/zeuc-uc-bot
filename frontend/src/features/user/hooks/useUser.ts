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
      if (user) {
        setUserCredentials(user);
        navigate(ERouteNames.CATALOG_PAGE);
      }
    }
  }, []);
};
