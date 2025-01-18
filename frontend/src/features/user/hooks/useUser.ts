import { useActions } from "@/shared/hooks/useActions";
import { useEffect } from "react";

export const useTelegramUser = () => {
  const { setUserCredentials } = useActions();

  useEffect(() => {
    // if (window.Telegram) {
    //   const user = window.Telegram.WebApp.initDataUnsafe?.user;
      const mockUser = { id: 5163648472, username: "magoxdd" };
    //   if (mockUser) {
        setUserCredentials(mockUser);
    //   }
  }, []);
};
