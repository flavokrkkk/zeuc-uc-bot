import { useState } from "react";
import { toast } from "sonner";

export const useCopied = (textToCopy: string) => {
  const [isCopied, setIsCopied] = useState(false);
  const handleCopyClick = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
      toast.error("Скопировано", {
        position: "top-center",
      });
    } catch (err) {
      toast.error(`Не удалось скопировать ${err}`, {
        position: "top-center",
      });
      console.error("Ошибка при копировании текста:", err);
      setIsCopied(false);
    }
  };

  return {
    isCopied,
    handleCopyClick,
  };
};
