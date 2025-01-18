import { useActions } from "@/shared/hooks/useActions";
import { useEffect } from "react";

export const useTelegramUser = () => {
  const { setUserCredentials } = useActions();

  useEffect(() => {
    if (window.Telegram) {
      const user = window.Telegram.WebApp.initDataUnsafe?.user;
      if (user) {
        setUserCredentials(user);
      }
    }
  }, []);
};
