import { getAllPacks } from "@/entities/packs/libs/packsService";
import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useQuery } from "@tanstack/react-query";
import { useCallback } from "react";
import { useNavigate } from "react-router-dom";

export const usePacks = () => {
  const navigate = useNavigate();
  const isSelected = useAppSelector(packSlectors.isSelected);
  const packs = useAppSelector(packSlectors.getPackSelects);
  const totalPrice = useAppSelector(packSlectors.totalPrice);

  const {
    setSelectPacks,
    setSelectedPacks,
    resetTotalPacks,
    setUnSelectPacks,
    setPacks,
  } = useActions();

  const { data, isSuccess } = useQuery({
    queryKey: ["packs"],
    queryFn: (meta) => getAllPacks(meta),
  });

  if (isSuccess) {
    setPacks(data);
  }

  const handleSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setSelectPacks(Number(event.currentTarget.value));
    },
    []
  );

  const handleUnSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setUnSelectPacks(Number(event.currentTarget.value));
    },
    []
  );

  const handleSelectPacks = () => {
    setSelectedPacks();
    navigate(ERouteNames.PAYMENT_PAGE, { replace: true });
  };

  const handleResetTotalPacks = () => resetTotalPacks();

  return {
    isSelected,
    packs,
    totalPrice,
    handleSelectPack,
    handleUnSelectPack,
    handleSelectPacks,
    handleResetTotalPacks,
  };
};
