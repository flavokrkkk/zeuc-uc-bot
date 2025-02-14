import { FC } from "react";
import ReactDOM from "react-dom";

interface IModal {
  children: React.ReactNode;
  isOpen: boolean;
  onClose?: () => void;
}

const Modal: FC<IModal> = ({ children, isOpen, onClose }) => {
  const changeModalContent = (
    event: React.MouseEvent<HTMLDivElement, MouseEvent>
  ) => {
    event.stopPropagation();
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div
      onClick={onClose}
      className={`top-0 left-0 z-50 fixed h-screen w-screen bg-[#00000066] flex items-center justify-center ${
        isOpen
          ? "opacity-100 pointer-events-auto"
          : "opacity-0 pointer-events-none"
      }`}
    >
      <div
        className="bg-transparent absolute p-2 rounded-2xl"
        onClick={changeModalContent}
      >
        <div>{children}</div>
      </div>
    </div>,
    document.body
  );
};

export default Modal;
