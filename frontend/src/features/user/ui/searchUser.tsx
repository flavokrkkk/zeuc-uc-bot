import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { Input } from "@/shared/ui/input/input";
import { FC } from "react";

interface ISearchUser {
  isLabel?: boolean;
  searchPlaceholder: string;
  buttonText: string;
}

const SearchUser: FC<ISearchUser> = ({
  isLabel = true,
  buttonText,
  searchPlaceholder,
}) => {
  return (
    <section className="flex items-center justify-between">
      {isLabel && <h1>Ваш ID</h1>}
      <span>
        <Input className="border-none" placeholder={searchPlaceholder} />
      </span>
      <span>
        <Button
          className="px-4"
          rounded={ButtonRoundSizes.ROUNDED_LG}
          bgColor={ButtonColors.GREEN}
        >
          {buttonText}
        </Button>
      </span>
    </section>
  );
};

export default SearchUser;
