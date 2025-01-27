/* eslint-disable @typescript-eslint/ban-ts-comment */
import { IPack } from "@/entities/packs/types/types";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import clsx from "clsx";
import { FC, useState } from "react";
import { useSwipeable } from "react-swipeable";
import "../styles/pack.css";
import { Trash2Icon } from "lucide-react";
interface IPacksBadge {
  pack: IPack;
  handleDeletePack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksBadge: FC<IPacksBadge> = ({
  pack,
  handleDeletePack,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  const [angleSwipe, setAngleSwipe] = useState<"right" | "left" | "">("");
  const handlers = useSwipeable({
    onSwipedLeft: () => {
      setAngleSwipe("left");
    },
    onSwipedRight: () => {
      setAngleSwipe("right");
    },
    //@ts-ignore
    preventDefaultTouchmoveEvent: true,
    trackMouse: true,
  });

  return (
    <div
      key={pack.id}
      className={clsx(
        "bg-dark-200 swipeable-element h-[48px] p-1 rounded-lg flex items-center justify-between",
        angleSwipe === "left" && "swipe-left pl-5",
        angleSwipe !== "left" && "px-5 "
      )}
      {...handlers}
    >
      <div className="flex space-x-2 items-center">
        <span>{pack.uc_amount}</span>
        <span>
          <Icon type={IconTypes.UC_OUTLINED} />
        </span>
      </div>
      <div className="bg-gray-dark-100 w-[94px] h-[32px] flex items-center justify-between px-2 rounded-lg">
        <button
          disabled={pack.multiplication_uc === 1}
          value={pack.id}
          className="rounded-lg flex items-center justify-center cursor-pointer h-full w-full"
          onClick={handleUnSelectPack}
        >
          <Icon type={IconTypes.MINUS_OUTLINED} />
        </button>

        <button className="rounded-lg h-full w-full">
          {pack.multiplication_uc}
        </button>
        <button
          value={pack.id}
          className="rounded-lg cursor-pointer h-full w-full flex items-center justify-center"
          onClick={handleSelectPack}
        >
          <Icon type={IconTypes.PLUS_OUTLINED} />
        </button>
      </div>
      <div className="space-x-1 text-white">
        <span>{pack.price_per_uc.price} рублей</span>
      </div>
      {angleSwipe === "left" && (
        <button
          className="h-full bg-red-500 rounded-lg px-4 text-xs flex items-center flex-col justify-center"
          value={pack.id}
          onClick={handleDeletePack}
        >
          <Trash2Icon className="h-4 w-4" />
          <span>Удалить</span>
        </button>
      )}
    </div>
  );
};
export default PacksBadge;
