import { getCurrentUser } from "@/entities/user/libs/userService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";

export const useUser = () => {
  const { setCurrentUser } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["currentuser"],
    queryFn: (meta) => getCurrentUser(meta),
  });

  if (isSuccess) {
    setCurrentUser(data);
  }
};
