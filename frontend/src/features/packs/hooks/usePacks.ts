import { packSlectors } from "@/entities/uc/model/store/packSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const usePacks = () => {
  const navigate = useNavigate();
  const isSelected = useAppSelector(packSlectors.isSelected);
  const packs = useAppSelector(packSlectors.getPackSelects);
  const totalPrice = useAppSelector(packSlectors.totalPrice);

  const { setSelectPacks, setSelectedPacks } = useActions();

  const handleSelectPack = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
    setSelectPacks(Number(event.currentTarget.value));
  };

  const handleSelectPacks = () => {
    setSelectedPacks();
    navigate(ERouteNames.PAYMENT_PAGE, { replace: true });
  };

  useEffect(() => {
    if (window.Telegram) {
      window.Telegram.WebApp.init();

      const user = window.Telegram.WebApp.initDataUnsafe?.user;
      if (user) {
        console.log("User Info:", user);
        alert(JSON.stringify(user));
      }
      const language = window.Telegram.WebApp.initDataUnsafe?.lang;
      console.log("Language:", language);
    }
  }, []);

  return { isSelected, packs, totalPrice, handleSelectPack, handleSelectPacks };
};
