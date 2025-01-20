import { IPack } from "@/entities/packs/types/types";
import { FC } from "react";
import PacksCard from "./packsCard";

interface IPacksList {
  packs: Array<IPack>;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksList: FC<IPacksList> = ({ packs, handleSelectPack }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 p-1">
      {packs.map((card) => (
        <PacksCard card={card} handleSelectPack={handleSelectPack} />
      ))}
    </div>
  );
};

export default PacksList;
