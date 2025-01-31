import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useCallback } from "react";
import { useNavigate } from "react-router-dom";

export const usePacks = () => {
  const navigate = useNavigate();
  const isSelected = useAppSelector(packSlectors.isSelected);
  const packs = useAppSelector(packSlectors.getPackSelects);
  const totalPrice = useAppSelector(packSlectors.totalPrice);
  const totalPacks = useAppSelector(packSlectors.totalPacks);

  const {
    setSelectPacks,
    setSelectedPacks,
    resetTotalPacks,
    setUnSelectPacks,
  } = useActions();

  const handleSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setSelectPacks(event.currentTarget.value);
    },
    [setSelectPacks]
  );

  const handleUnSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setUnSelectPacks({ id: event.currentTarget.value, type: "count" });
    },
    []
  );

  const handleSelectPacks = () => {
    setSelectedPacks();
    navigate(ERouteNames.PAYMENT_PAGE);
  };

  const handleResetTotalPacks = () => resetTotalPacks();

  return {
    isSelected,
    packs,
    totalPrice,
    totalPacks,
    handleSelectPack,
    handleUnSelectPack,
    handleSelectPacks,
    handleResetTotalPacks,
  };
};
