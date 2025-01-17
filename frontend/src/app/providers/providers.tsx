import { RouterProvider } from "react-router-dom";
import { routes } from "../pages/routes";
import { Provider } from "react-redux";
import { store } from "@/shared/store";

const Providers = () => {
  return (
    <Provider store={store}>
      <RouterProvider router={routes} />
    </Provider>
  );
};

export default Providers;
