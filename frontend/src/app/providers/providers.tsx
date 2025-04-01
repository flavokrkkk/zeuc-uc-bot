import { RouterProvider } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "@/shared/store";
import { routes } from "@/pages/routes";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/shared/api/queryClient";
import { ViewerProvider } from "@/entities/viewer/models/context/providers";
import { Toaster } from "sonner";

const Providers = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ViewerProvider>
        <Provider store={store}>
          <RouterProvider router={routes} />
          <Toaster />
        </Provider>
      </ViewerProvider>
    </QueryClientProvider>
  );
};

export default Providers;
