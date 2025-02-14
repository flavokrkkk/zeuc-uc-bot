import { createBrowserRouter, Navigate, Outlet } from "react-router-dom";
import RootPage from "./rootPage";
import ErrorPage from "./errorPage";
import { Suspense } from "react";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { privatePage } from "@/entities/viewer/libs/hoc/privatePage";
import { routesWithHoc } from "./routes/routesWithHoc";
import { publicPage } from "@/entities/viewer/libs/hoc/publicPage";
import MainPage from "./mainPage";
import CatalogPage from "./catalogPage";
import PaymentPage from "./paymentPage";
import ReferalPage from "./referalPage";
import TicketsPage from "./ticketsPage";
import ScoresPage from "./scoresPage";
import HistoryPaymentPage from "./historyPaymentPage";
import BonusPaymentPage from "./bonusPaymentPage";

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
              path: ERouteNames.BONUS_PAYMENT_PAGE,
              element: <BonusPaymentPage />,
            },
            {
              path: ERouteNames.PAYMENT_HISTORY_PAGE,
              element: <HistoryPaymentPage />,
            },
            {
              path: ERouteNames.SCORES_PAGE,
              element: <ScoresPage />,
            },
          ]),
        ],
      },
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
          element: <ErrorPage />,
        },
        {
          path: ERouteNames.CLOSE_ERROR,
          element: <ErrorPage message="В данный момент магазин закрыт" />,
        },
      ]),
    ],
  },
]);
