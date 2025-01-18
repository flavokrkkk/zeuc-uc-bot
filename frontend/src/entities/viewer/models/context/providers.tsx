import {
  createContext,
  FC,
  PropsWithChildren,
  useContext,
  useEffect,
  useState,
} from "react";
import { IViewerHandler, IViewerState } from "../types";
import {
  deleteAccessToken,
  getAccessToken,
  setAccessToken,
} from "@/entities/token/libs/tokenService";

const ViewerContext = createContext<IViewerState & IViewerHandler>({
  isAuthenticated: false,
  loginViewer: () => {},
  logoutViewer: () => {},
});

export const useViewer = () => {
  return useContext(ViewerContext);
};

export const ViewerProvider: FC<PropsWithChildren> = ({ children }) => {
  const [viewer, setViewer] = useState<IViewerState>({
    isAuthenticated: false,
  });
  const handleLoginViewer = (accessToken: string) => {
    setViewer({
      isAuthenticated: true,
      accessToken,
    });
    setAccessToken(accessToken);
  };

  const handleLogoutViewer = () => {
    setViewer({
      isAuthenticated: false,
      accessToken: null,
    });
    deleteAccessToken();
  };

  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      setViewer({
        isAuthenticated: true,
        accessToken: token,
      });
    }
  }, []);

  return (
    <ViewerContext.Provider
      value={{
        ...viewer,
        loginViewer: handleLoginViewer,
        logoutViewer: handleLogoutViewer,
      }}
    >
      {children}
    </ViewerContext.Provider>
  );
};
