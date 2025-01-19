import { packActions } from "@/entities/packs/model/store/packSlice";
import { scoresActions } from "@/entities/scores/models/store/scoresSlice";
import { userActions } from "@/entities/user/models/store/userSlice";
import { bindActionCreators } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";

export const useActions = () => {
  const dispatch = useDispatch();

  return bindActionCreators(
    { ...packActions, ...userActions, ...scoresActions },
    dispatch
  );
};
