function showToast(title, message, type = "normal", duration = 3000) {
  const toast = document.getElementById("toast-component");
  const tTitle = document.getElementById("toast-title");
  const tMsg   = document.getElementById("toast-message");
  if (!toast) return;

  const color = {
    success: ["bg-green-50","border-green-500","text-green-700"],
    error: ["bg-red-50","border-red-500","text-red-700"],
    normal: ["bg-white","border-gray-300","text-gray-800"]
  };

  toast.className = `fixed bottom-5 right-5 z-[9999] px-4 py-3 rounded-lg border shadow-lg transition-all duration-300 opacity-0 translate-y-64 ${
    color[type].join(' ')
  }`;

  tTitle.textContent = title;
  tMsg.textContent = message;

  // Animate in
  toast.classList.remove('opacity-0','translate-y-64');
  toast.classList.add('opacity-100','translate-y-0');

  // Auto-hide
  setTimeout(() => {
    toast.classList.add('opacity-0','translate-y-64');
    toast.classList.remove('opacity-100','translate-y-0');
  }, duration);
}