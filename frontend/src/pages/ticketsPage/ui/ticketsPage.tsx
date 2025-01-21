import TicketsContent from "@/features/referals/ui/ticketsContent";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "../../../shared/ui/button/button";

const TicketsPage = () => {
  return (
    <section className="w-full pt-2 space-y-6">
      <TicketsContent />
      <div>
        <Button
          className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
          bgColor={ButtonColors.GREEN}
          rounded={ButtonRoundSizes.ROUNDED_XL}
        >
          Использовать бонусы
        </Button>
      </div>
    </section>
  );
};

export default TicketsPage;
