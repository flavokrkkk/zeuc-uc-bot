import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { Input } from "@/shared/ui/input/input";
import clsx from "clsx";
import { FC } from "react";

interface ISearchUser {
  value?: string;
  isLabel?: boolean;
  error: "success" | "error" | "";
  searchPlaceholder: string;
  buttonText: string;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const SearchUser: FC<ISearchUser> = ({
  value = "",
  isLabel = true,
  error,
  buttonText,
  searchPlaceholder,
  onChange = () => {},
  onClick = () => {},
}) => {
  return (
    <section className="flex items-center justify-between">
      {isLabel && <h1>Ваш ID</h1>}
      <span className="">
        <Input
          value={value}
          className={clsx(
            error === "error"
              ? "border-red-600"
              : error === "success"
              ? "border-green-600"
              : "border-none"
          )}
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
