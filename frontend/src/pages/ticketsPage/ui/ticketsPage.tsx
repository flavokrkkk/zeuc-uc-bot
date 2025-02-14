import TicketsContent from "@/features/referals/ui/ticketsContent";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "../../../shared/ui/button/button";
import { useTickets } from "@/features/referals/hooks/useTickets";
import { useNavigate } from "react-router-dom";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";

const TicketsPage = () => {
  useTickets();

  const navigate = useNavigate();

  const handleNavigate = () => navigate(ERouteNames.SCORES_PAGE);
  return (
    <section className="w-full pt-2 space-y-6">
      <TicketsContent />
      <div>
        <Button
          className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
          bgColor={ButtonColors.GREEN}
          onClick={handleNavigate}
          rounded={ButtonRoundSizes.ROUNDED_XL}
        >
          Использовать бонусы
        </Button>
      </div>
    </section>
  );
};

export default TicketsPage;
