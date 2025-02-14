import { useActions } from "@/shared/hooks/useActions";
import { useEffect } from "react";

export const useUser = (isAuthenticated: boolean) => {
  const { getAsyncCurrentUser, getAsyncDiscount } = useActions();

  useEffect(() => {
    if (isAuthenticated) {
      getAsyncCurrentUser();
      getAsyncDiscount();
    }
  }, [isAuthenticated]);
};
