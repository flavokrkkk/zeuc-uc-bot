import SearchUser from "@/features/user/ui/searchUser";
import { Copy } from "lucide-react";

const ReferalContent = () => {
  return (
    <section className="space-y-10">
      <h1 className="text-2xl">Приглашайте друзей и получайте кредиты!</h1>
      <p>
        Поделитесь кодом на приглашение с друзьями. И вы, и ваш приглашенный
        получите <span className="text-yellow-400">20 бонусов</span>, когда они
        зарегистрируются.
      </p>
      <div className="bg-dark-200 space-y-2 flex-col p-4 px-6  rounded-md flex justify-between">
        <section className="items-center rounded-md flex justify-between space-x-5">
          <div>cnfUa4KY99cnfUa4KY99cnfU</div>
          <span>
            <Copy className="cursor-pointer" />
          </span>
        </section>
      </div>
      <div className="space-y-4">
        <h1 className="text-2xl">
          Введите реферальный код, чтобы получить бонусы
        </h1>
        <SearchUser
          isLabel={false}
          buttonText="Активировать"
          searchPlaceholder="Введите код"
        />
      </div>
    </section>
  );
};

export default ReferalContent;
