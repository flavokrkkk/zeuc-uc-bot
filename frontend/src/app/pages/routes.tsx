import { createBrowserRouter, Navigate } from "react-router-dom";
import RootPage from "./rootPage";
import ErrorPage from "./errorPage";
import { lazy } from "react";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";

const CatalogPage = lazy(() => import("../pages/catalogPage"));
const PaymentPage = lazy(() => import("../pages/paymentPage"));

export const routes = createBrowserRouter([
  {
    element: <RootPage />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
        element: <Navigate to={ERouteNames.CATALOG_PAGE} replace />,
      },
      {
        path: ERouteNames.CATALOG_PAGE,
        element: <CatalogPage />,
      },
      {
        path: ERouteNames.PAYMENT_PAGE,
        element: <PaymentPage />,
      },
    ],
  },
]);
