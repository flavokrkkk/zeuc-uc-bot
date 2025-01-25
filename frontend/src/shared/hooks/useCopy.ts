import { useState } from "react";

export const useCopied = (textToCopy: string) => {
  const [isCopied, setIsCopied] = useState(false);
  const handleCopyClick = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error("Ошибка при копировании текста:", err);
      setIsCopied(false);
    }
  };

  return {
    isCopied,
    handleCopyClick,
  };
};
