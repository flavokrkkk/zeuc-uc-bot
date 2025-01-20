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
const PaymentHistoryPage = lazy(() => import("@pages/historyPaymentPage"));
const ScoresPage = lazy(() => import("@pages/scoresPage"));
const ReferalPage = lazy(() => import("@pages/referalPage"));
const TicketsPage = lazy(() => import("@pages/ticketsPage"));
const MainPage = lazy(() => import("@pages/mainPage"));

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <RootPage />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
        element: <Navigate to={"/main"} replace />,
      },
      {
        path: "/main",
        element: <MainPage />,
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
            {
              path: ERouteNames.REFERAL_PAGE,
              element: <ReferalPage />,
            },
            {
              path: ERouteNames.TICKETS_PAGE,
              element: <TicketsPage />,
            },
            {
              path: ERouteNames.PAYMENT_HISTORY_PAGE,
              element: <PaymentHistoryPage />,
            },
            {
              path: ERouteNames.SCORES_PAGE,
              element: <ScoresPage />,
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
    ],
  },
]);
