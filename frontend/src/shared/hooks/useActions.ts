import { packActions } from "@/entities/uc/model/store/packSlice";
import { bindActionCreators } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";

export const useActions = () => {
  const dispatch = useDispatch();

  return bindActionCreators({ ...packActions }, dispatch);
};
