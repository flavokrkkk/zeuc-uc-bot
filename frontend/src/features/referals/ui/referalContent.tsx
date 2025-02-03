import { userSelectors } from "@/entities/user/models/store/userSlice";
import SearchUser from "@/features/user/ui/searchUser";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useCopied } from "@/shared/hooks/useCopy";
import clsx from "clsx";
import { Copy } from "lucide-react";
import { useReferal } from "../hooks/useReferal";
import { useCallback, useState } from "react";

const ReferalContent = () => {
  const [referalCode, setReferalCode] = useState("");
  const currentUser = useAppSelector(userSelectors.currentUser);
  const { handleReferalActivate, referalError } = useReferal();

  const { isCopied, handleCopyClick } = useCopied(
    currentUser?.referal_code ?? ""
  );

  const handleChangeCode = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setReferalCode(event.target.value);
    },
    []
  );

  return (
    <section className="space-y-10">
      <h1 className="text-2xl">Приглашайте друзей и получайте кредиты!</h1>
      <p>
        Поделитесь кодом на приглашение с друзьями. И вы, и ваш приглашенный
        получите <span className="text-yellow-400">20 бонусов</span>, когда они
        зарегистрируются.
      </p>
      <div className="bg-dark-200 space-y-2 flex-col p-4 px-6  rounded-xl flex justify-between">
        <section className="items-center rounded-md flex justify-between space-x-5">
          <button>{currentUser?.referal_code}</button>
          <button
            className={clsx(
              "w-5 h-5 text-dark-600 cursor-pointer transition-transform",
              isCopied ? "text-green-700 animate-pulseOnce" : ""
            )}
            onClick={handleCopyClick}
          >
            <Copy />
          </button>
        </section>
      </div>
      <div className="space-y-4">
        <h1 className="text-2xl">
          Введите реферальный код, чтобы получить бонусы
        </h1>
        <SearchUser
          value={referalCode}
          isLabel={false}
          error={referalError}
          buttonText="Активировать"
          searchPlaceholder="Введите код"
          onChange={handleChangeCode}
          onClick={handleReferalActivate}
        />
      </div>
    </section>
  );
};

export default ReferalContent;
