import UcOutlined from "../../../../../public/icons/uc-outlined.svg";
import PointOutlined from "../../../../../public/icons/point-outlined.svg";
import BgOutlined from "../../../../../public/icons/bg-outlined.svg";
import BgUcOutlined from "../../../../../public/icons/uc-bg-outlined.svg";
import MinusOutlined from "../../../../../public/icons/minus-outlined.svg";
import PlusOutlined from "../../../../../public/icons/plus-outlined.svg";
import BagsOutlined from "../../../../../public/icons/bags-outlined.svg";
import ReferalOutlined from "../../../../../public/icons/referal-outlined.svg";
import ScoreOutlined from "../../../../../public/icons/score-outlined.svg";
import TicketsOutlined from "../../../../../public/icons/tickets-outline.svg";
import DollarOutlined from "../../../../../public/icons/dollar-outlined.svg";
import SbpOutlined from "../../../../../public/icons/sbp-outlined.svg";
import ShopOutlined from "../../../../../public/icons/shop-outlined.svg";

export const enum IconTypes {
  UC_OUTLINED,
  POINT_OUTLINED,
  BG_OUTLINED,
  BG_UC_OUTLINED,
  AVATARKA_OUTLINED,
  MINUS_OUTLINED,
  PLUS_OUTLINED,
  BAGS_OUTLINED,
  REFERAL_OUTLINED,
  SCORE_OUTLINED,
  TICKETS_OUTLINED,
  DOLLAR_OUTLINED,
  SBP_OUTLINED,
  SHOP_OUTLINED,
}

export type IconDictionaryType = {
  [key in IconTypes]: string;
};

export const IconDictionary: Record<string, string> = {
  [IconTypes.UC_OUTLINED]: UcOutlined,
  [IconTypes.POINT_OUTLINED]: PointOutlined,
  [IconTypes.BG_OUTLINED]: BgOutlined,
  [IconTypes.BG_UC_OUTLINED]: BgUcOutlined,
  [IconTypes.MINUS_OUTLINED]: MinusOutlined,
  [IconTypes.PLUS_OUTLINED]: PlusOutlined,

  [IconTypes.BAGS_OUTLINED]: BagsOutlined,
  [IconTypes.REFERAL_OUTLINED]: ReferalOutlined,
  [IconTypes.TICKETS_OUTLINED]: TicketsOutlined,
  [IconTypes.SCORE_OUTLINED]: ScoreOutlined,
  [IconTypes.DOLLAR_OUTLINED]: DollarOutlined,
  [IconTypes.SBP_OUTLINED]: SbpOutlined,
  [IconTypes.SHOP_OUTLINED]: ShopOutlined,
};
export const enum IconSizes {
  SMALL,
  MEDIUM,
  LARGE,
}

interface IconSize {
  width: number;
  stroke: number;
}

export const IconSizeValues: Record<IconSizes, IconSize> = {
  [IconSizes.SMALL]: {
    width: 16,
    stroke: 1,
  },
  [IconSizes.MEDIUM]: {
    width: 24,
    stroke: 1.5,
  },
  [IconSizes.LARGE]: {
    width: 36,
    stroke: 2.25,
  },
};

export interface IconSizeWithHeight extends IconSize {
  height?: number;
}

export interface IResponsiveSizes {
  base?: IconSizeWithHeight;
  md?: IconSizeWithHeight;
  lg?: IconSizeWithHeight;
  xl?: IconSizeWithHeight;
  xxl?: IconSizeWithHeight;
}

export const enum IconRotation {
  DEG_0,
  DEG_45,
  DEG_90,
  DEG_180,
  DEG_270,
}

export const IconRotationClasses: Record<IconRotation, string> = {
  [IconRotation.DEG_0]: "rotate-0",
  [IconRotation.DEG_45]: "rotate-45",
  [IconRotation.DEG_90]: "rotate-90",
  [IconRotation.DEG_180]: "rotate-180",
  [IconRotation.DEG_270]: "rotate-270",
};
