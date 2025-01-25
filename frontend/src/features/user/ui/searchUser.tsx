import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { Input } from "@/shared/ui/input/input";
import { FC } from "react";

interface ISearchUser {
  value?: string;
  isLabel?: boolean;
  searchPlaceholder: string;
  buttonText: string;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const SearchUser: FC<ISearchUser> = ({
  value = "",
  isLabel = true,
  buttonText,
  searchPlaceholder,
  onChange = () => {},
  onClick = () => {},
}) => {
  return (
    <section className="flex items-center justify-between">
      {isLabel && <h1>Ваш ID</h1>}
      <span className="w-[132px]">
        <Input
          value={value}
          className="border-none"
          placeholder={searchPlaceholder}
          onChange={onChange}
        />
      </span>
      <span>
        <Button
          value={value}
          isDisabled={!value}
          className="px-4"
          rounded={ButtonRoundSizes.ROUNDED_LG}
          bgColor={ButtonColors.GREEN}
          onClick={onClick}
        >
          {buttonText}
        </Button>
      </span>
    </section>
  );
};

export default SearchUser;
