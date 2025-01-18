import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";
import RootPage from "./rootPage";
import ErrorPage from "./errorPage";
import { lazy, Suspense } from "react";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { privatePage } from "@/entities/viewer/libs/hoc/privatePage";
import { routesWithHoc } from "./routes/routesWithHoc";
import { publicPage } from "@/entities/viewer/libs/hoc/publicPage";

const CatalogPage = lazy(() => import("@pages/catalogPage"));
const PaymentPage = lazy(() => import("@pages/paymentPage"));

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <RootPage />,
    errorElement: <ErrorPage />,
    children: [
      ...routesWithHoc(privatePage, [
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
      ]),
    ],
  },
  {
    path: ERouteNames.AUTH_PAGE,
    element: (
      <Suspense fallback={<div className="h-screen w-full">Loading..</div>}>
        <Outlet />
      </Suspense>
    ),
    children: [
      ...routesWithHoc(publicPage, [
        {
          path: "",
          element: <Navigate to={ERouteNames.AUTH_ERROR} replace />,
        },
        {
          path: ERouteNames.AUTH_ERROR,
          element: (
            <div className="flex justify-center bg-purple-00 items-center w-full h-full">
              <h1 className="text-purple-400 font-medium text-2xl">
                Вход не возможен! Повторите попытку
              </h1>
            </div>
          ),
        },
      ]),
    ],
  },
]);
