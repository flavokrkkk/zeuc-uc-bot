import { IPack } from "@/entities/packs/types/types";
import { FC } from "react";

interface IPacksList {
  packs: Array<IPack>;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksList: FC<IPacksList> = ({ packs, handleSelectPack }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 p-1">
      {packs.map((card) => (
        <div key={card.id} className="w-full space-y-1">
          <div className="h-20 px-4 flex-col w-full  аcursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md">
            {`${card.ucinitial} UC (x${card.multiplication_uc})`}

            <button
              className="h-10 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
              value={card.id}
              onClick={handleSelectPack}
            >
              Выбрать
            </button>
          </div>
          {/* {!!card.multiplication_uc && (
            <div className="flex space-x-1">
              <button value={card.id} onClick={handleSelectPack}>
                +
              </button>
              <button
                value={card.id}
                className="h-10 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
                onClick={setUnSelectPacks}
              >
                -
              </button>
            </div>
          )} */}
        </div>
      ))}
    </div>
  );
};

export default PacksList;
