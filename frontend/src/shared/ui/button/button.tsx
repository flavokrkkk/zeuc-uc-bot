import clsx from "clsx";
import React, { FC, HTMLAttributes, ReactElement, memo } from "react";

export enum ButtonColors {
  WHITE,
  BLACK,
  TRANSPARENT_BLACK,
  DODGER_BLUE,
  GREEN,
}

export enum ButtonSizes {
  LARGE,
  MEDIUM,
  SMALL,
}
export enum ButtonBorderSizes {
  NONE,
  BORDER_SM,
  BORDER_MD,
  BORDER_LG,
  BORDER_XL,
}

export enum ButtonBorderColors {
  SILVER,
}

export enum ButtonRoundSizes {
  NONE,
  ROUNDED_SM,
  ROUNDED,
  ROUNDED_3PX,
  ROUNDED_MD,
  ROUNDED_LG,
  ROUNDED_XL,
  ROUNDED_2XL,
  ROUNDED_FULL,
}

interface IButtonClasses {
  activeClasses: string;
  disableClasses: string;
}

export const ButtonColorClasses: Record<ButtonColors, IButtonClasses> = {
  [ButtonColors.DODGER_BLUE]: {
    activeClasses: "bg-dodger-blue text-white",
    disableClasses: "bg-gray-300 text-gray-500",
  },
  [ButtonColors.WHITE]: {
    activeClasses: "bg-white text-black",
    disableClasses: "bg-gray-300 text-gray-500",
  },
  [ButtonColors.BLACK]: {
    activeClasses: "bg-dark-300 text-white",
    disableClasses: "bg-gray-300 text-gray-500",
  },
  [ButtonColors.GREEN]: {
    activeClasses: "bg-green-100 text-white",
    disableClasses: "bg-gray-300 text-gray-500",
  },
  [ButtonColors.TRANSPARENT_BLACK]: {
    activeClasses: "bg-transparent text-white",
    disableClasses: "bg-gray-300 text-gray-500",
  },
};

export const ButtonSizeClasses: Record<ButtonSizes, string> = {
  [ButtonSizes.LARGE]: "px-[95px] py-[6px] text-base",
  [ButtonSizes.MEDIUM]: "p-6",
  [ButtonSizes.SMALL]: "p-2",
};
export const ButtonBorderSizeClasses: Record<ButtonBorderSizes, string> = {
  [ButtonBorderSizes.NONE]: "border-0",
  [ButtonBorderSizes.BORDER_SM]: "border",
  [ButtonBorderSizes.BORDER_MD]: "border-2",
  [ButtonBorderSizes.BORDER_LG]: "border-[3px]",
  [ButtonBorderSizes.BORDER_XL]: "border-4",
};

export const ButtonBorderColorClasses: Record<ButtonBorderColors, string> = {
  [ButtonBorderColors.SILVER]: "border-silver",
};

export const ButtonRoundSizeClasses: Record<ButtonRoundSizes, string> = {
  [ButtonRoundSizes.NONE]: "rounded-none",
  [ButtonRoundSizes.ROUNDED_SM]: "rounded-sm",
  [ButtonRoundSizes.ROUNDED_3PX]: "rounded-[3px]",
  [ButtonRoundSizes.ROUNDED]: "rounded",
  [ButtonRoundSizes.ROUNDED_MD]: "rounded-md",
  [ButtonRoundSizes.ROUNDED_LG]: "rounded-lg",
  [ButtonRoundSizes.ROUNDED_XL]: "rounded-xl",
  [ButtonRoundSizes.ROUNDED_2XL]: "rounded-2xl",
  [ButtonRoundSizes.ROUNDED_FULL]: "rounded-full",
};
export enum ButtonTypes {
  BUTTON = "button",
  RESET = "reset",
  SUBMIT = "submit",
}

export interface ButtonProps extends HTMLAttributes<HTMLButtonElement> {
  text?: string;
  className?: string;
  isDisabled?: boolean;
  value?: string;
  image?: string;
  isLoading?: boolean;
  iconLeft?: ReactElement | null;
  iconRight?: ReactElement | null;
  onClick?: (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
  size?: ButtonSizes;
  type?: ButtonTypes;
  bgColor?: ButtonColors;
  rounded?: ButtonRoundSizes;
  borderSize?: ButtonBorderSizes;
  borderColors?: ButtonBorderColors;
  children?: React.ReactNode;
}

export const Button: FC<ButtonProps> = memo(
  ({
    onClick,
    className,
    isDisabled,
    type = ButtonTypes.BUTTON,
    size = ButtonSizes.SMALL,
    bgColor = ButtonColors.BLACK,
    rounded = ButtonRoundSizes.NONE,
    borderSize = ButtonBorderSizes.NONE,
    borderColors = ButtonBorderColors.SILVER,
    value,
    children,
  }) => (
    <button
      value={value && value}
      className={clsx(
        `
      flex items-center justify-center transition-all 
      
      ${ButtonSizeClasses[size]}
      ${
        ButtonColorClasses[bgColor][
          isDisabled ? "disableClasses" : "activeClasses"
        ]
      }
      ${ButtonRoundSizeClasses[rounded]}
      ${ButtonBorderSizeClasses[borderSize]}
			${ButtonBorderColorClasses[borderColors]}
      
    `,
        className && className
      )}
      disabled={isDisabled}
      onClick={onClick}
      type={type}
    >
      {children}
    </button>
  )
);
