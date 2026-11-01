import client from "@/library/ApiClient";
import store from "@/store/index";

interface IMenu {
  label: string;
  icon: string;
  iconActive: string;
  route: string;
  tooltip: string;
  subMenu: Menu[];
}
class Menu implements IMenu {
  constructor(
    public label: string,
    public icon: string,
    public iconActive: string,
    public route: string,
    public tooltip: string,
    public subMenu: Menu[] = []
  ) {}
}

export function mGetMenu() {
  return client
    .CheckRoleMenuByUserId({
      store: store,
      data: {
        username: store.state.username,
      },
    })
    .then((response) => {
      switch (response.plainData.responseCode) {
        case "011000": {
          const menus = response.plainData.responseData.roleMenuList ?? [];
          const listMenu: Menu[] = [];
          menus.forEach((element) => {
            const icon = "/images/sidebar/" + element.iconName + ".png";
            const iconActive = "/images/sidebar/" + element.iconName + "A.png";
            const listSubMenu: Menu[] = [];

            if (element?.subMenu?.length) {
              element.subMenu.forEach((sub_element) => {
                listSubMenu.push(
                  new Menu(
                    sub_element.label,
                    icon,
                    iconActive,
                    sub_element.route,
                    sub_element.tooltip,
                    sub_element.subMenu
                  )
                );
              });
            }

            listMenu.push(
              new Menu(
                element.label,
                icon,
                iconActive,
                element.route,
                element.tooltip,
                listSubMenu
              )
            );
          });

          return {
            createworkspace:
              response.plainData.responseData.createworkspace ?? false,
            menus: listMenu,
          };
        }
        default: {
          return {
            createworkspace: false,
            menus: [],
          };
        }
      }
    });
}
