import { ucActions } from "@/entities/uc/model/store/ucSlice";
import { bindActionCreators } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";

export const useActions = () => {
  const dispatch = useDispatch();

  return bindActionCreators({ ...ucActions }, dispatch);
};
