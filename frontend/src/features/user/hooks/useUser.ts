import {
  getCurrentUser,
  getUserDiscount,
} from "@/entities/user/libs/userService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

export const useUser = (isAuthenticated: boolean) => {
  const { setCurrentUser, setUserDiscount } = useActions();
  const { data: userData, isSuccess } = useQuery({
    queryKey: ["currentuser"],
    queryFn: (meta) => getCurrentUser(meta),
    enabled: isAuthenticated,
  });

  const { data: discountData, isSuccess: isDiscountSuccess } = useQuery({
    queryKey: ["discount"],
    queryFn: (meta) => getUserDiscount(meta),
    enabled: isAuthenticated,
  });

  useEffect(() => {
    if (isSuccess && isDiscountSuccess) {
      setCurrentUser(userData);
      setUserDiscount(discountData);
    }
  }, [userData, discountData, isSuccess, isDiscountSuccess]);
};
