import { getAllPacks } from "@/entities/packs/libs/packsService";
import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect } from "react";
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
    setPacks,
  } = useActions();

  const { data, isSuccess } = useQuery({
    queryKey: ["packs"],
    queryFn: (meta) => getAllPacks(meta),
  });

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
      setUnSelectPacks(event.currentTarget.value);
    },
    []
  );

  const handleSelectPacks = () => {
    setSelectedPacks();
    navigate(ERouteNames.PAYMENT_PAGE, { replace: true });
  };

  const handleResetTotalPacks = () => resetTotalPacks();

  useEffect(() => {
    if (isSuccess && data) {
      setPacks(data);
    }
  }, [isSuccess, data]);

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
