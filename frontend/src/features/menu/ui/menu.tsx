import { pathNavigate } from "@/shared/libs/utils/pathNavigate";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { FC } from "react";
import { NavLink } from "react-router-dom";

interface IMenu {
  navigates: typeof pathNavigate;
}

const Menu: FC<IMenu> = ({ navigates }) => {
  return (
    <div className="flex w-full justify-between">
      {navigates.map((nav) => (
        <NavLink
          className={({ isActive }) =>
            isActive ? "text-green-600" : "text-white"
          }
          key={nav.id}
          to={nav.path}
        >
          <Icon type={nav.icon} />
        </NavLink>
      ))}
    </div>
  );
};

export default Menu;
