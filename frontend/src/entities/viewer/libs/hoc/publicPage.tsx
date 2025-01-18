import { FC, PropsWithChildren, useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";
import { useViewer } from "../../models/context/providers";
import { getAccessToken } from "@/entities/token/libs/tokenService";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";

export const publicPage = (children: React.ReactNode) => {
  return <PublicPage>{children}</PublicPage>;
};

const PublicPage: FC<PropsWithChildren> = ({ children }) => {
  const { loginViewer } = useViewer();
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getAccessToken();

    if (token) {
      loginViewer(token);
      navigate(ERouteNames.CATALOG_PAGE);
    } else {
      setIsLoading(false);
    }
  }, [loginViewer, navigate]);

  if (isLoading) {
    return <h1>Loading....</h1>;
  }

  return children;
};
