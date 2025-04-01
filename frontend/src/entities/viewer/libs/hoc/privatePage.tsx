import { FC, PropsWithChildren, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useViewer } from "../../models/context/providers";
import {
  getAccessToken,
  getStateCloseShop,
} from "@/entities/token/libs/tokenService";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";

export const privatePage = (children: React.ReactNode) => {
  return <PrivatePage>{children}</PrivatePage>;
};

const PrivatePage: FC<PropsWithChildren> = ({ children }) => {
  const navigate = useNavigate();
  const { isAuthenticated, loginViewer } = useViewer();
  const pathname = useLocation();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = getAccessToken();
    const shopState = getStateCloseShop();
    if (token) {
      loginViewer(token);
      setIsLoading(false);
    } else {
      setIsLoading(false);
      if (!shopState) {
        navigate(ERouteNames.CLOSE_ERROR);
        return;
      }
      navigate(ERouteNames.AUTH_ERROR);
    }
  }, [pathname]);

  if (isLoading) {
    return <h1>Loading....</h1>;
  }

  return isAuthenticated ? children : null;
};
